import requests
from bs4 import BeautifulSoup

URL = 'https://realpython.github.io/fake-jobs/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')  
cards = soup.find_all("div", class_="card")

for card in cards:
    #print(card.find())
    title = card.find("h2", class_="title").text.strip()
    company = card.find('h3', class_='company').text.strip()
    location = card.find('p', class_='location').text.strip()
    time = card.find('time').text.strip()

    print(f'{title} at {company} in {location}')
