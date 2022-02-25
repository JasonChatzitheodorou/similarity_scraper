import requests
from bs4 import BeautifulSoup

artist = 'Mark_Lanegan'
URL = 'https://en.wikipedia.org/wiki/' + artist
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser') 

infobox = soup.find('table', class_='infobox')

associated_acts = infobox.find('span', string='Associated acts').parent.next_sibling 
associated_acts = associated_acts.find_all('a')
links_to_associated = {associated.text.strip(): associated['href'] for associated in associated_acts}
for assoc in links_to_associated:
    print(assoc)
