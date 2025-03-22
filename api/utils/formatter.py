import re
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
    # Basic dictionary of known word-values (cardinals + ordinals)
    number_values = {
        # Cardinals
        'zero': 0,
        'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
        'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
        'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19,
        'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
        'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90,
        'hundred': 100, 'thousand': 1000,

        # Ordinals (map to same numeric value as cardinal)
        'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5,
        'sixth': 6, 'seventh': 7, 'eighth': 8, 'ninth': 9, 'tenth': 10,
        'eleventh': 11, 'twelfth': 12, 'thirteenth': 13, 'fourteenth': 14,
        'fifteenth': 15, 'sixteenth': 16, 'seventeenth': 17, 'eighteenth': 18,
        'nineteenth': 19, 'twentieth': 20, 'thirtieth': 30, 'fortieth': 40,
        'fiftieth': 50, 'sixtieth': 60, 'seventieth': 70, 'eightieth': 80,
        'ninetieth': 90, 'hundredth': 100, 'thousandth': 1000,
    }

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

    def parse_number_phrase(phrase: str) -> str:
        """
        Convert an English spelled-out number phrase (possibly containing ordinals)
        into its digit form. Safeguards against converting 'and' alone to '0'.
        """
        phrase_lower = phrase.lower()
        tokens = phrase_lower.split()

        # Expand hyphens (e.g. "twenty-five" -> ["twenty","five"])
        expanded = []
        for tok in tokens:
            if '-' in tok:
                expanded.extend(tok.split('-'))
            else:
                expanded.append(tok)

        # Replace "a" -> "one" but skip "and"
        filtered = [("one" if w == "a" else w) for w in expanded if w != "and"]

        # If no recognized numeric tokens remain, return original phrase
        if not any(w in number_values for w in filtered):
            return phrase  # <-- This prevents "and" from becoming "0"

        total = 0
        current = 0
        for w in filtered:
            if w in number_values:
                val = number_values[w]
                if val >= 100:
                    if current == 0:
                        current = 1
                    current *= val
                    # Add immediately for thousand/million/etc.
                    if val >= 1000:
                        total += current
                        current = 0
                else:
                    current += val
            # Unknown tokens are just skipped

        numeric_value = total + current

        # Check if final token is an ordinal word (e.g. "seventh", "hundredth")
        if filtered and filtered[-1] in ordinal_words:
            return str(numeric_value) + ordinal_suffix(numeric_value)
        else:
            return str(numeric_value)

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
        # Convert with the new parser
        return parse_number_phrase(phrase)

    # Do the substitution
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

    # Example context patterns:
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