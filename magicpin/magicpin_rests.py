from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import requests
import MySQLdb

db = MySQLdb.connect(host="",
                     user="",
                     passwd="",
                     db="")

cur = db.cursor()

cur.execute('select url from test')
existing_urls = cur.fetchall()
existing_urls = list(existing_urls)
actual_urls = []
for x in existing_urls:
    actual_urls.append(list(x))

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
current_page = 1
last_page = 931
data = []
while True:
    url = f"https://magicpin.in/india/Jaipur/All/Restaurant/?page={current_page}"
    print(f'Current page: {url} | {current_page}/931')

    page = requests.get(url, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    for parent in soup.find_all(class_='merchant-card-single'):
        url = parent.find('a')
        if url != None:
            url = url.attrs['href']
        else:
            continue
        name = parent.find(class_='merchant-name')
        name = name.get_text()
        location = parent.find(class_='merchant-location')
        if location != None:
            location = location.get_text()
        else:
            location = "None"
        rating = parent.find(class_='rating-value')
        if rating != None:
            rating = rating.get_text()
        else:
            rating = "None"
        price = parent.find(class_='detail-value avg-spend')
        if price != None:
            price = price.get_text()
            price = f"Average Customer Spend : {price}"
        else:
            price = 'None'
        
        cuisine = parent.find(class_='details')
        if cuisine != None:
            a_tag = cuisine.find('span', class_='detail-value')
            if a_tag != None:
                cuisine = a_tag.get_text()
            else:
                cuisine = "None"
        else:
            cuisine = "None"
        offer = parent.find(class_='cashback')
        if offer != None:
            offer = offer.get_text()
        else:
            offer = "None"
        print(name)
        print(url)
        print(rating)
        print(location)
        print(price)
        print(cuisine)
        print(offer)
        item = [name, url, cuisine, price, rating, location, offer]
        data.append(item)
    current_page += 1
    if current_page>last_page:
        break


df = pd.DataFrame(data, columns=['Name', 'Url', 'Cuisine', 'Price', 'Rating', 'location', 'offer'])
df.to_excel('magicpin_rests.xlsx', index=True)