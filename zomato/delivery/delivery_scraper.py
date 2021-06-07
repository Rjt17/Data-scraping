import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

# Web scrapper for infinite scrolling page 
driver = webdriver.Chrome(executable_path=r"D:\chromedriver.exe")
driver.get("https://www.zomato.com/jaipur/restaurants?category=15")
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1
while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break
"""(screen_height) * i > scroll_height"""
data = []
soup = BeautifulSoup(driver.page_source, "html.parser")
for parent in soup.find_all(class_="sc-eSePXt kCSfyN"):
    a_tag = parent.find("a", class_="sc-guztPN cmYbqu")
    pro_offer = a_tag.find("p", class_="sc-1hez2tp-0 sc-fvLVrH dqPsdZ")
    simple_offer = a_tag.find("p", class_="sc-1hez2tp-0 sc-fvLVrH Mwdyz")
    second_a_tag = parent.find("a", class_="sc-jRhVzh bJMzNa")
    cuisine = second_a_tag.find("p", class_="sc-1hez2tp-0 sc-hkbPbT nslib")
    price = second_a_tag.find(class_="sc-bYnzgO fxfkIf")
    rating = second_a_tag.find(class_="sc-1hez2tp-0 lhdg1m-2 dgzDPB")
    new_rests = second_a_tag.find(class_="sc-2gamf4-0 fSJGVb")
    no_reviews = second_a_tag.find(class_="sc-1hez2tp-0 lhdg1m-8 hztxkg")
    name = second_a_tag.find(class_="sc-1hez2tp-0 sc-hcnlBt yRyBD")
    base = "https://www.zomato.com/jaipur/delivery"
    link = a_tag.attrs['href']
    url = urljoin(base, link)
    if name != None:
        name = name.get_text()
    else:
        name = "None"
    if pro_offer != None:
        pro_offer = pro_offer.get_text()
    else:
        pro_offer = "None"
    if simple_offer != None:
        simple_offer = simple_offer.get_text()
    else:
        simple_offer = "None"
    if cuisine != None:
        cuisine = cuisine.get_text()
    else:
        cuisine = "None"
    if price != None:
        price = price.get_text()
    else:
        price = "None"
    if rating != None:
        rating = rating.get_text()
    else:
        rating = "None"
    if new_rests != None:
        new_rests = new_rests.get_text()
    else:
        new_rests = "None"
    if no_reviews != None:
        no_reviews = no_reviews.get_text()
    else:
        no_reviews = "None"
    item = [name, url, cuisine, price, rating, new_rests, no_reviews]
    data.append(item)
print(data)


df = pd.DataFrame(data, columns = ['Name', 'Url', 'Cuisine', 'Price', 'Rating', 'New', 'Reviews'])
df.to_excel('delivery_rest_zomato_urls.xlsx', index = True)
