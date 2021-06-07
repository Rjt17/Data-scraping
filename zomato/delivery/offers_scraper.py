import openpyxl
import requests
from requests.api import request
from bs4 import BeautifulSoup
import pandas as pd

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

workbook = openpyxl.load_workbook('delivery_rest_zomato.xlsx')
sheet = workbook.active
rest_urls = []
for url in sheet['C']:
    rest_urls.append(url.value)
rest_urls.remove('Url')
i=1
data = []
offer_url= []
offer_list = []
for url in rest_urls:
    print(f'Working Url: {url} : {i}/1461')
    i+=1
    page = requests.get(url, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    for parent in soup.find_all(class_='sc-1a03l6b-2 dJyJVg'):
        offer = parent.find(class_='sc-1a03l6b-0 lkqupg')
        code = parent.find(class_='sc-1a03l6b-1 kvnZBD')
        if offer != None:
            offer = offer.get_text()
        else:
            offer = "None"
        if code != None:
            code = code.get_text()
        else:
            code = "None"
        temp_list = [offer, code]
        offer_list.append(temp_list)    
    for parent in soup.find_all(class_='sc-1a03l6b-2 fNMWNE'):
        pro_offer = parent.find(class_='sc-1a03l6b-0 lkqupg')
        if pro_offer != None:
            pro_offer = pro_offer.get_text()
        else:
            pro_offer = 'None'
        offer_list.append(pro_offer)
    for parent in soup.find_all(class_='sc-bnXvFD wdvhv'):
        location = parent.find(class_='sc-jzgbtB grxiHO')
        if location != None:
            location = location.get_text()
        else:
            location = None
    offer_url = [url, location, offer_list]
    data.append(offer_url)
    offer_url = []
    offer_list = []
print(data)
df = pd.DataFrame(data, columns=['url', 'location', 'offers'])
df.to_excel('offer_delivery.xlsx', index = True)