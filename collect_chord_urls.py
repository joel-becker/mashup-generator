import requests

url = 'https://www.ultimate-guitar.com/explore?order=hitstotal_desc&type[]=Chords'
response = requests.get(url)
html_content = response.text

from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')