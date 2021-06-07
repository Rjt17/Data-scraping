from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import requests

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
current_page = 1
last_page = 10

data = []
while True:
    url = f"https://www.dineout.co.in/jaipur-restaurants?p={current_page}"
    print(f'Current page: {url}')
    page = requests.get(url, headers=headers)
    content = page.content

    soup = BeautifulSoup(content, "html.parser")
    for parent in soup.find_all(class_='restnt-card restaurant'):
        rating = parent.find(class_='restnt-rating')
        a_tag = parent.find(class_='restnt-name ellipsis')
        location = parent.find(class_='restnt-loc ellipsis')
        price_cuisine = parent.find(class_='double-line-ellipsis')
        dineout_pay = parent.find(class_='btn pay cursor')
        if a_tag != None:
            name = a_tag.get_text()
            base = 'https://www.dineout.co.in/jaipur/'
            url = a_tag.attrs['href']
            url = urljoin(base,url)
        else:
            continue
        if rating != None:
            rating = rating.get_text()
        else:
            rating = 'None'
        if location != None:
            location = location.get_text()
        else:
            location = 'None'
        if price_cuisine != None:
            price_cuisine = price_cuisine.get_text()
            temp_list = price_cuisine.split('|')
            price = temp_list[0]
            cuisine = temp_list[-1]
        else:
            price_cuisine = 'None'
            price = 'None'
            cuisine = 'None'
        if dineout_pay != None:
            dineout_pay = dineout_pay.get_text()
        else:
            dineout_pay = 'None'
        offer = 'None'
        for child in parent.find_all(class_='offers-info-wrap'):
            if child != None:
                offer = child.find(class_='double-line-ellipsis')
                if offer != None:
                    offer = offer.get_text()
                else:
                    offer = "None"
            else:
                offer = 'None'
        print(name)
        print(url)
        print(rating)
        print(location)
        print(price)
        print(cuisine)
        print(dineout_pay)
        print(offer)
        item = [name, url, cuisine, price, rating, location, dineout_pay, offer]
        data.append(item)

    current_page += 1
    for parent in soup.find_all(class_='listing-pagination'):
        pages = parent.find_all('a')
        page = pages[-2]
        page = int(page.get_text())
        print(page)
    if (page % 10) != 0:
        last_page = page
    else:
        last_page = 1000
    if current_page> last_page:
        break


df = pd.DataFrame(data, columns=['Name', 'Url', 'Cuisine', 'Price', 'Rating', 'location', 'dineout pay', 'offer'])
df.to_excel('dineout_rests.xlsx', index=True)