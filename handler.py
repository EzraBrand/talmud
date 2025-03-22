import json
import re
import requests
from word2number import w2n

# Dictionary for terminology preferences
TERMINOLOGY_PREFERENCES = {
    r'\bGemara\b': 'Talmud',
    r'\bRabbi\b': 'R\'',
    r'\bThe Sages taught\b': 'A baraita states',
    r'\bDivine Voice\b': 'bat kol',
    r'\bDivine Presence\b': 'Shekhina',
    r'\bdivine inspiration\b': 'Holy Spirit',
    r'\bthe Lord\b': 'YHWH',
    r'\bleper\b': 'metzora',
    r'\bleprosy\b': 'tzara\'at',
    r'\bphylacteries\b': 'tefillin',
    r'\bgentile\b': 'non-Jew',
    r'\bignorant\b': 'am ha\'aretz',
    r'\bignoram(us|i)\b': 'am ha\'aretz',
    r'\bmaidservant\b': 'female slave',
    r'\bbarrel\b': 'jug',
}

# API Handler
def get_text(event, context):
    try:
        # Parse the incoming request body
        body = json.loads(event.get('body', '{}'))
        
        # Get parameters from request
        reference = body.get('reference', '')
        language = body.get('language', 'all')
        remove_nikud_marks = body.get('remove_nikud', True)
        standardize_terms = body.get('standardize_terms', True)
        split_sentences = body.get('split_sentences', True)
        include_adjacent = body.get('include_adjacent', False)
        adjacent_pages = body.get('adjacent_pages', 0)
        
        # Initialize response
        result = {
            'success': False,
            'message': '',
            'content': []
        }
        
        # Get the main text data
        main_data = query_sefaria(reference, language)
        
        if not main_data:
            result['message'] = f"No data found for reference: {reference}"
            return create_response(result)
        
        # Process the main text
        processed_main = process_sefaria_data(main_data, remove_nikud_marks, standardize_terms, split_sentences)
        result['content'].append({
            'title': f"Current Page ({reference})",
            'sections': processed_main
        })
        
        # Get adjacent pages if requested
        if include_adjacent and adjacent_pages > 0:
            # Get previous and next pages
            prev_pages = []
            next_pages = []
            
            current_ref = reference
            # Get previous pages
            for i in range(adjacent_pages):
                prev_ref, _ = get_adjacent_pages(current_ref)
                if prev_ref:
                    prev_data = query_sefaria(prev_ref, language)
                    if prev_data:
                        processed_prev = process_sefaria_data(prev_data, remove_nikud_marks, standardize_terms, split_sentences)
                        prev_pages.append({
                            'title': f"Previous Page ({prev_ref})",
                            'sections': processed_prev,
                            'reference': prev_ref
                        })
                    current_ref = prev_ref
            
            # Reset to original reference
            current_ref = reference
            # Get next pages
            for i in range(adjacent_pages):
                _, next_ref = get_adjacent_pages(current_ref)
                if next_ref:
                    next_data = query_sefaria(next_ref, language)
                    if next_data:
                        processed_next = process_sefaria_data(next_data, remove_nikud_marks, standardize_terms, split_sentences)
                        next_pages.append({
                            'title': f"Next Page ({next_ref})",
                            'sections': processed_next,
                            'reference': next_ref
                        })
                    current_ref = next_ref
            
            # Add pages in proper order (prev -> current -> next)
            result['content'] = list(reversed(prev_pages)) + result['content'] + next_pages
        
        result['success'] = True
        
    except Exception as e:
        result = {
            'success': False,
            'message': f"Error: {str(e)}",
            'content': []
        }
    
    return create_response(result)

def create_response(body):
    """Create a proper response with CORS headers"""
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }

# Sefaria API Functions
def query_sefaria(ref, language="all"):
    """Query the Sefaria API for a specific text reference."""
    # Format the reference for the API
    formatted_ref = ref.replace(" ", "_")

    # Construct the API URL
    base_url = "https://www.sefaria.org/api/texts/"
    url = f"{base_url}{formatted_ref}"

    # Add parameters for language
    params = {
        "context": 0,
        "language": language,
    }

    # Make the request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_adjacent_pages(ref):
    """Determine the previous and next pages for a given Talmud reference."""
    # Parse the reference to extract tractate and page
    if '.' not in ref:
        return None, None

    parts = ref.split('.')
    tractate = parts[0]
    page_info = parts[1]

    # Handle different page formats (e.g., "2a", "10b")
    page_number = ''.join(filter(str.isdigit, page_info))
    page_side = 'a' if page_info[-1] == 'a' else 'b'

    # Calculate previous page
    prev_page = None
    if page_side == 'b':
        # If current is "Xb", previous is "Xa"
        prev_page = f"{tractate}.{page_number}a"
    elif int(page_number) > 2:  # Talmud typically starts at 2a
        # If current is "Xa", previous is "(X-1)b"
        prev_page = f"{tractate}.{int(page_number)-1}b"

    # Calculate next page
    next_page = None
    if page_side == 'a':
        # If current is "Xa", next is "Xb"
        next_page = f"{tractate}.{page_number}b"
    else:
        # If current is "Xb", next is "(X+1)a"
        next_page = f"{tractate}.{int(page_number)+1}a"

    return prev_page, next_page

# Text Processing Functions
def remove_nikud(text):
    """Remove Hebrew vowel marks (nikud) while preserving standard punctuation."""
    if not text:
        return text
    return re.sub(r'[\u0591-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7]', '', text)

def standardize_terminology(text):
    """Standardize terminology according to preferred terms with improved number handling."""
    if not text:
        return text

    # Apply terminology preferences first
    for pattern, replacement in TERMINOLOGY_PREFERENCES.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # Define helper data/functions to parse spelled-out numbers safely
    # Words that specifically indicate an ordinal form
    ordinal_words = {
        'first', 'second',
        'third', 'fourth', 'fifth',
        'sixth', 'seventh', 'eighth', 'ninth', 'tenth',
        'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth',
        'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth',
        'twentieth', 'thirtieth', 'fortieth', 'fiftieth',
        'sixtieth', 'seventieth', 'eightieth', 'ninetieth',
        'hundredth', 'thousandth',
    }

    def ordinal_suffix(n: int) -> str:
        """Return the appropriate English ordinal suffix for the integer n."""
        if 11 <= (n % 100) <= 13:
            return "th"
        last_digit = n % 10
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(last_digit, 'th')

    # Pattern to match any "spelled-out" number phrase
    number_word_pattern = re.compile(
        r'\b(?:a|one|two|three|four|five|six|seven|eight|nine|ten|'
        r'eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|'
        r'eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|'
        r'eighty|ninety|hundred|thousand|million|billion|trillion|'
        r'first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|'
        r'eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|'
        r'seventeenth|eighteenth|nineteenth|twentieth|thirtieth|fortieth|'
        r'fiftieth|sixtieth|seventieth|eightieth|ninetieth|hundredth|'
        r'thousandth|millionth|billionth|trillionth)(?:-[a-zA-Z]+)?'
        r'(?:\s+(?:a|one|two|three|four|five|six|seven|eight|nine|ten|'
        r'eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|'
        r'eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|'
        r'eighty|ninety|hundred|thousand|million|billion|trillion|'
        r'first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|'
        r'eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|'
        r'seventeenth|eighteenth|nineteenth|twentieth|thirtieth|fortieth|'
        r'fiftieth|sixtieth|seventieth|eightieth|ninetieth|hundredth|'
        r'thousandth)(?:-[a-zA-Z]+)?)*\b',
        flags=re.IGNORECASE
    )
    
    def convert_number_words(match):
        # Grab the entire matched phrase
        phrase = match.group(0)
        # Convert using word2number safely
        try:
            # Check if it's an ordinal word
            if any(word in phrase.lower().split() for word in ordinal_words):
                # Convert to number first, then add ordinal suffix
                # Handle multi-word ordinals like "twenty-first"
                text_with_hyphens = phrase.lower().replace(' ', '-')
                for ordinal in ordinal_words:
                    if text_with_hyphens.endswith(f"-{ordinal}"):
                        base = text_with_hyphens[:-(len(ordinal)+1)]
                        try:
                            num = w2n.word_to_num(base.replace('-', ' '))
                            return f"{num}{ordinal_suffix(num)}"
                        except ValueError:
                            return phrase
                
                # Direct conversion for single ordinals
                try:
                    # Remove "th", "st", etc. for word2number
                    if phrase.lower() in ordinal_words:
                        # Single ordinal word like "first"
                        clean_phrase = phrase
                        if clean_phrase.lower() == "first":
                            return "1st"
                        elif clean_phrase.lower() == "second":
                            return "2nd"
                        elif clean_phrase.lower() == "third":
                            return "3rd"
                        else:
                            # Convert numeric part, then add suffix
                            word_base = clean_phrase.lower()
                            if word_base.endswith("th"):
                                word_base = word_base[:-2]
                            try:
                                num = w2n.word_to_num(word_base)
                                return f"{num}{ordinal_suffix(num)}"
                            except ValueError:
                                return phrase
                except ValueError:
                    return phrase
            else:
                # Regular cardinal number
                try:
                    num = w2n.word_to_num(phrase)
                    return str(num)
                except ValueError:
                    return phrase
        except (ValueError, AttributeError):
            return phrase

    # Do the substitution for numbers
    text = re.sub(number_word_pattern, convert_number_words, text)

    # Handle numeric ordinals in certain contexts
    def add_ordinal_suffix(match):
        num = int(match.group(1))
        # English ordinal suffix logic
        if 10 <= num % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(num % 10, 'th')
        return f"{num}{suffix}"

    # Example context patterns
    text = re.sub(r'the (\d+) day', lambda m: f"the {add_ordinal_suffix(m)} day", text)
    text = re.sub(r'(\d+) century', lambda m: f"{add_ordinal_suffix(m)} century", text)

    return text

def split_by_punctuation(text):
    """Split text by periods, colons, and question marks while preserving punctuation."""
    if not text:
        return []

    # Split by periods, colons, and question marks
    # This regex looks for these punctuation marks followed by a space or end of string
    splits = re.split(r'([.?:](?:\s|$))', text)

    # Recombine the split results to keep the punctuation with the preceding text
    result = []
    i = 0
    while i < len(splits):
        if i + 1 < len(splits) and any(splits[i+1].startswith(p) for p in ['.', '?', ':']):
            combined = splits[i] + splits[i+1]
            result.append(combined.strip())
            i += 2
        else:
            if splits[i].strip():  # Only add non-empty segments
                result.append(splits[i].strip())
            i += 1

    return result

def process_sefaria_data(data, remove_nikud_marks, standardize_terms, split_sentences):
    """Process the Sefaria API data and return formatted sections."""
    sections = []
    
    # Process Hebrew text if needed
    hebrew_text = None
    if 'he' in data and data['he']:
        if remove_nikud_marks:
            if isinstance(data['he'], list):
                hebrew_text = [remove_nikud(line) for line in data['he']]
            else:
                hebrew_text = remove_nikud(data['he'])
        else:
            hebrew_text = data['he']
    
    # Process English text if needed
    english_text = None
    if 'text' in data and data['text']:
        if standardize_terms:
            if isinstance(data['text'], list):
                english_text = [standardize_terminology(line) for line in data['text']]
            else:
                english_text = standardize_terminology(data['text'])
        else:
            english_text = data['text']
    
    # Format into sections
    if isinstance(english_text, list) and isinstance(hebrew_text, list):
        for i, (heb, eng) in enumerate(zip(hebrew_text, english_text)):
            # Split text if requested
            if split_sentences:
                heb_lines = split_by_punctuation(heb)
                eng_lines = split_by_punctuation(eng)
            else:
                heb_lines = [heb]
                eng_lines = [eng]
            
            sections.append({
                'number': i + 1,
                'hebrew': heb_lines,
                'english': eng_lines
            })
    elif english_text and hebrew_text:
        # Single item case
        if split_sentences:
            heb_lines = split_by_punctuation(hebrew_text)
            eng_lines = split_by_punctuation(english_text)
        else:
            heb_lines = [hebrew_text]
            eng_lines = [english_text]
        
        sections.append({
            'number': 1,
            'hebrew': heb_lines,
            'english': eng_lines
        })
    
    return sections