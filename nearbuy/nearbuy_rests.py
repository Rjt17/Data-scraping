from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import requests
import time

initial_url = "https://www.nearbuy.com/jaipur/collection/all-restaurants-offer"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

urls = []

page = requests.get(initial_url, headers=headers)
content = page.content

soup = BeautifulSoup(content, "html.parser")
for parent in soup.find_all(class_='card-main card-main--equal-height cursor-pointer'):
    link = parent.attrs['href']
    base = 'https://www.nearbuy.com/'
    url = urljoin(base, link)
    urls.append(url)
    offer = parent.find_all('p')
    offer = offer[-2]
    offer = offer.get_text()
    offer = offer[29:-124] + " from" + offer[-60:-54]
    name = parent.find('h2')
    location = name.find('span')
    name = name.get_text()
    location = location.get_text()
    name = name[21:-30]
    print(name)