from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import requests

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
last_page = 8
current_page = 1
data = []
while True:
    url = f"https://www.swiggy.com/jaipur?page={current_page}"
    print(f'Current page: {url}')
    page = requests.get(url, headers=headers)
    content = page.content

    soup = BeautifulSoup(content, "html.parser")
    for parent in soup.find_all(class_='MZy1T'):
        for child in parent.find_all(class_='_3XX_A'):
            a_tag = child.find('a')
            name = child.find(class_='nA6kb')
            cuisine = child.find(class_='_1gURR')
            rating = child.find(class_='_9uwBC wY0my')
            price = child.find(class_='nVWSi')
            
            base = 'https://www.swiggy.com/'
            if a_tag == None:
                continue
            link = a_tag.attrs['href']
            url = urljoin(base, link)
            name = name.get_text()
            cuisine = cuisine.get_text()
            if rating != None:
                rating = rating.get_text()
            else:
                rating = "None"
            price = price.get_text()
            
            item = [name, url, cuisine, price, rating]
            data.append(item)

    all_pages = soup.find_all(class_='_1FZ7A')
    if last_page == []:
        last_page = current_page + 1
        continue
    last_page = all_pages[-1]
    last_page = int(last_page.get_text())
    current_page += 1
    if last_page < current_page:
        break

df = pd.DataFrame(data, columns=['Name', 'Url', 'Cuisine', 'Price', 'Rating'])
df.to_excel('swiggy_rests.xlsx', index=True)