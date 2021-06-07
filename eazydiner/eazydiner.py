from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import MySQLdb

db = MySQLdb.connect(host="#",
                     user="#",
                     passwd="#",
                     db="#")

cur = db.cursor()

cur.execute('select url from test')
existing_urls = cur.fetchall()
existing_urls = list(existing_urls)
actual_urls = []
for x in existing_urls:
    actual_urls.append(list(x))

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
current_page = 1
last_page = 100

while True:
    url = f"https://www.eazydiner.com/jaipur/restaurants?page={current_page}"
    print(f'Current page: {url}')
    page = requests.get(url, headers=headers)
    content = page.content

    soup = BeautifulSoup(content, "html.parser")
    if current_page == 1:
        for parent in soup.find_all(class_='pagination'):
            pages =  parent.find_all('li')
            page = pages[-2]
            page = page.get_text()
            last_page = int(page)
            
    for parent in soup.find_all(class_='padding-10 radius-4 bg-white restaurant margin-b-10'):
        a_tag = parent.find(class_='apxor_click')
        name = parent.find('span', class_='res_name')
        location = parent.find('span', class_='res_loc inline-block')
        price = parent.find(class_='padding-l-10 grey cost_for_two')
        cuisine = parent.find(class_='padding-l-10 grey res_cuisine')
        offer = parent.find('span', class_='grey bold deal_name')
        rating = parent.find(class_='critic')

        if a_tag != None:
            base = 'https://www.eazydiner.com/jaipur/'
            a_tag = a_tag.attrs['href']
            url = urljoin(base, a_tag)
        else:
            a_tag = 'None'
            continue
        name = name.get_text()
        if location != None:
            location = location.get_text()
        else:
            location = 'None'
        if price != None:
            price = price.get_text()
        else:
            price = 'None'
        if cuisine != None:
            cuisine = cuisine.get_text()
        else:
            cuisine = 'None'
        if offer != None:
            offer = offer.get_text()
            offer = offer[50:-21]
        else:
            offer = 'None'
        if rating != None:
            rating = rating.get_text()
            rating = rating[1:]
        else:
            rating = 'None'
        
        extra_url = url
        extra_offer = offer
        name = name.encode("utf-8")
        url = url.encode("utf-8")
        location = location
        price = price.encode("utf-8")
        cuisine = cuisine
        offer = offer
        rating = rating
        

        #updates offers
        cur.execute('select offer from test where url = %s', [url])
        sql_offer_url = cur.fetchall()
        if sql_offer_url != ():
            for x in sql_offer_url:
                sql_offer_url = list(x)
            if [offer] != sql_offer_url:
                print([offer])
                print(sql_offer_url)
                cur.execute('delete from test where url = %s', [url])
                actual_urls.remove([extra_url])

            
        #adds restaurants
        item = [name, url, cuisine, price, rating, location, offer]
        if [extra_url] in actual_urls:
            continue
        cur.execute("insert into test values(%s, %s, %s, %s, %s, %s, %s)", item)

    current_page += 1
    if current_page>last_page:
        db.commit()
        db.close()
        break
