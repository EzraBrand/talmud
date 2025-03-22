import requests

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