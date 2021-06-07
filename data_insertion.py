from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import MySQLdb
from requests.models import RequestEncodingMixin

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

db = MySQLdb.connect(host="#",
                     user="#",
                     passwd="#",
                     db="#")

cur = db.cursor()

#####
#eazydiner
"""
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
        name = name
        url = url.encode("utf-8")
        location = location
        price = price
        cuisine = cuisine
        offer = offer
        rating = rating
        dineout_pay = "None"


        print(url)
        cur.execute("select id from restaurant where ezzee_dinner_url = %s", [extra_url])
        id = cur.fetchone()
        if id != None:
            id = list(id)
            id = id[0]
            print(id)
            cur.execute("update restaurant_comparison set ezze_dinner_offer = %s where restuarant_id = %s", [offer, id])
            db.commit()
            print('updated')

        else:
            cur.execute("select url from restaurants_extra where url = %s", [extra_url])
            restaurants_extra_url = cur.fetchone()
            if restaurants_extra_url == None:
                price = list(price)
                for x in price:
                    if x == "₹":
                        price.remove("₹")
                current_price = ""
                for x in price:
                    current_price += x
                offer = list(offer)
                for x in offer:
                    if x == "₹":
                        offer.remove("₹")
                current_offers = ""
                for x in offer:
                    current_offers += x
                item = [name, extra_url, cuisine, current_price, rating, location,dineout_pay, current_offers]
                cur.execute("insert into restaurants_extra values(%s, %s, %s, %s, %s, %s, %s, %s)", item)
                db.commit()
                print('adding data to rests')
    current_page += 1
    if current_page> last_page:
        break
"""

############
#dineout
"""
current_page = 1
last_page = 100
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

        print(url)
        cur.execute("select id from restaurant where dineout_url = %s", [url])
        id = cur.fetchone()
        if id != None:
            id = list(id)
            id = id[0]
            print(id)
            cur.execute("update restaurant_comparison set dineout_offer = %s where restuarant_id = %s", [offer, id])
            db.commit()
            print('updated')

        else:
            cur.execute("select url from restaurants_extra where url = %s", [url])
            restaurants_extra_url = cur.fetchone()
            if restaurants_extra_url == None:
                price = list(price)
                for x in price:
                    if x == "₹":
                        price.remove("₹")
                current_price = ""
                for x in price:
                    current_price += x
                offer = list(offer)
                for x in offer:
                    if x == "₹":
                        offer.remove("₹")
                current_offers = ""
                for x in offer:
                    current_offers += x
                item = [name, url, cuisine, current_price, rating, location, dineout_pay, current_offers]
                cur.execute("insert into restaurants_extra values(%s, %s, %s, %s, %s, %s, %s, %s)", item)
                db.commit()
                print('adding data to rests')

        item = [name, url, cuisine, price, rating, location, dineout_pay, offer]

    current_page += 1
    try:
        for parent in soup.find_all(class_='listing-pagination'):
            pages = parent.find_all('a')
            page = pages[-2]
            page = int(page.get_text())
            print(page)
        if (page % 10) != 0:
            last_page = page
        else:
            last_page = 1000
    except:
        last_page = 1000
    if current_page> last_page:
        break
"""

######
#swiggy

last_page = 8
current_page = 1
urls = []
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
            dineout_pay = "None"
            location = "None"
            item = [name, url, cuisine, price, rating]

            print(url)
            offers = []
            new_page = requests.get(url, headers=headers)
            new_content = new_page.content
            soup1 = BeautifulSoup(new_content, "html.parser")
            found = soup1.find_all(class_='_3lvLZ')
            if found == []:
                offer = 'None'
                offers.append(offer)
                cur.execute("select id from restaurant where swiggy_url = %s", [url])
                id = cur.fetchone()
                if id != None:
                    id = list(id)
                    id = id[0]
                    print(id)
                    cur.execute("update restaurant_comparison set swiggy_offer = %s where restuarant_id = %s", [offers, id])
                    db.commit()
                    print('updated')
                else:
                    cur.execute("select url from restaurants_extra where url = %s", [url])
                    restaurants_extra_url = cur.fetchone()
                    if restaurants_extra_url == None:
                        price = list(price)
                        for x in price:
                            if x == "₹":
                                price.remove("₹")
                        current_price = ""
                        for x in price:
                            current_price += x
                        offer = list(offer)
                        for x in offer:
                            if x == "₹":
                                offer.remove("₹")
                        current_offers = ""
                        for x in offer:
                            current_offers += x
                        item = [name, url, cuisine, current_price, rating, location, dineout_pay, current_offers]
                        cur.execute("insert into restaurants_extra values(%s, %s, %s, %s, %s, %s, %s, %s)", item)
                        db.commit()
                    print('adding data to rests')

            else:
                for parent in found:
                    offer = parent.get_text()
                    offers.append(offer)
                offers = ','.join(offers)
                offers = list(offers)
                for x in offers:
                    if x == "₹":
                        offers.remove("₹")
                current_offers = ""
                for x in offers:
                    current_offers += x
                print(current_offers)
                cur.execute("select id from restaurant where swiggy_url = %s", [url])
                id = cur.fetchone()
                if id != None:
                    id = list(id)
                    id = id[0]
                    print(id)
                    cur.execute("update restaurant_comparison set swiggy_offer = %s where restuarant_id = %s", [current_offers, id])
                    db.commit()
                    print('updated')
                else:
                    cur.execute("select url from restaurants_extra where url = %s", [url])
                    restaurants_extra_url = cur.fetchone()
                    if restaurants_extra_url == None:
                        price = list(price)
                        for x in price:
                            if x == "₹":
                                price.remove("₹")
                        current_price = ""
                        for x in price:
                            current_price += x
                        item = [name, url, cuisine, current_price, rating, location, dineout_pay, current_offers]
                        cur.execute("insert into restaurants_extra values(%s, %s, %s, %s, %s, %s, %s, %s)", item)
                        db.commit()
                    print('adding data to rests')
                
    try:
        all_pages = soup.find_all(class_='_1FZ7A')
        if all_pages == None:
            last_page = current_page + 1
            continue
        if last_page == []:
            last_page = current_page + 1
            continue
        if last_page == None:
            last_page = current_page + 1
            continue
        last_page = all_pages[-1]
        last_page = int(last_page.get_text())
    except:
        last_page = current_page + 1
    current_page += 1
    if last_page < current_page:
            break


db.close()