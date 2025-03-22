from http.server import BaseHTTPRequestHandler
import json
import re
import requests
from word2number import w2n
from api.utils.formatter import remove_nikud, standardize_terminology, split_by_punctuation
from api.utils.sefaria_api import query_sefaria, get_adjacent_pages

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        # Read request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data)
        
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
        
        try:
            # Get the main text data
            main_data = query_sefaria(reference, language)
            
            if not main_data:
                result['message'] = f"No data found for reference: {reference}"
                self._send_response(result)
                return
            
            # Process the main text
            processed_main = self._process_sefaria_data(main_data, remove_nikud_marks, standardize_terms, split_sentences)
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
                            processed_prev = self._process_sefaria_data(prev_data, remove_nikud_marks, standardize_terms, split_sentences)
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
                            processed_next = self._process_sefaria_data(next_data, remove_nikud_marks, standardize_terms, split_sentences)
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
            result['message'] = f"Error: {str(e)}"
        
        self._send_response(result)

    def _send_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _process_sefaria_data(self, data, remove_nikud_marks, standardize_terms, split_sentences):
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
