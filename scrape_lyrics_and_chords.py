import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def get_html_content(url):
    """Fetch HTML content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

def extract_lyrics_and_chords(html_content):
    """Extract lyrics and chords from HTML content using BeautifulSoup and regex."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Use BeautifulSoup and regex to find the chords section
    start_index = str(soup).find("[Intro]")
    if start_index == -1:
        start_index = str(soup).find("[Verse 1]")
    try:
        end_indices = [m.start() for m in re.finditer(r'tab]&quot;,&quot;', str(soup))]
        if not end_indices:
            end_indices = [m.start() for m in re.finditer(r'tab]', str(soup))]
        end_index = end_indices[-1]
    except:
        end_index = len(str(soup))

    # Extract and clean up the chords section
    lyrics_and_chords = str(soup)[start_index:end_index]
    lyrics_and_chords = clean_lyrics_and_chords(lyrics_and_chords)
    
    return lyrics_and_chords

def clean_lyrics_and_chords(text):
    patterns = [
        #r'<script[^<]*?</script>',
        #r'<style[^<]*?</style>',
        #r'<!--.*?-->',
        #r'<[^>]+>',
        r'&nbsp;',
        r'<script>.*?</script>',
        r'<style>.*?</style>',
        r'&quot;',
        #r'&[a-z]+;',
        r'style="[^"]*"',
        r'<meta[^<]*?>',
        r'<link[^<]*?>',
        r'(name|href|src|alt|rel|as|property|content|title)=".*?"',
        r'\{[^}]*\}',
        #r'\[[^\]]*\]',
        r'\\r\\n+',
        r'\{*?\}',
        r'var sentryMethodsToSave.*?;',
        r'window\.Sentry = .*?;',
        r'var sentryLazyCallsQueue = .*?;',
        r'function .*?\(\) .*?;',
        r'sentryMethodsToSave.forEach\(function \(methodName\) .*?\);',
        r'window\.\w+ = .*?;',
        r'\w+\(\);',
        r':(true|false),',
        r'https://.*?,',
        r' : .*?.ultimate-guitar.com',
        #r'\|-.*?-\|',
        #r'\|',
        r'\s+'
    ]
    for pattern in patterns:
        text = re.sub(pattern, ' ', text, flags=re.DOTALL)
    return text.strip()

#def clean_lyrics_and_chords(text):
#    """Clean up the lyrics and chords text."""
#    text = re.sub(r'<script[^<]*?</script>', '', text, flags=re.DOTALL)
#    text = re.sub(r'<script[^<]*?</script>', '', text, flags=re.DOTALL)
#    text = re.sub(r'<style[^<]*?</style>', '', text, flags=re.DOTALL)
#    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
#    text = re.sub(r'&nbsp;', ' ', text)  # Replace non-breaking space
#    text = re.sub(r'&[a-z]+;', '', text) # Remove HTML entities
#    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
#    text = re.sub(r'style="[^"]*"', '', text)
#
#    text = re.sub(r'\<*?\/\>', '', text)  # Remove HTML tags
#    text = re.sub(r'\[.*?\]', '', text)  # Remove square bracket tags
#    text = re.sub(r'\{&q.*?\;}', '', text)  # Remove HTML entities
#    text = re.sub(r'\\r', ' ', text)  # Replace carriage return
#    text = re.sub(r'\|', ' ', text)  # Replace pipe characters with space
#    text = re.sub(r'&quot;', '', text)  # Remove HTML entities
#    text = re.sub(r'(name|href|src|alt|rel|as|property|content|title)=".*?"', '', text)  # Remove HTML attributes
#    return text.strip()  # Remove leading/trailing whitespace

def process_urls(url_list, verbose=True):
    """Process a list of URLs and return a DataFrame with URLs and cleaned lyrics/chords."""
    data = []  # To store tuples of (URL, Lyrics/Chords)
    
    for url in url_list:
        if verbose:
            print(f"Processing {url}...")
        html_content = get_html_content(url)
        if html_content:
            lyrics_and_chords = extract_lyrics_and_chords(html_content)
            data.append((url, lyrics_and_chords))
        else:
            data.append((url, "Failed to fetch content"))
    
    # Create a DataFrame from the collected data
    df = pd.DataFrame(data, columns=['URL', 'lyrics_and_chords'])
    return df