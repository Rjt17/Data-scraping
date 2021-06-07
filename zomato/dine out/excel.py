import openpyxl
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import pandas as pd


df = pd.read_excel(r'prices - Copy.xlsx')
dicts = df.to_dict('split')
data = dicts['data']
final_data = []
for x in data:
    name = x[0]
    price = x[-1]
    if pd.isnull(price) == True:
        price = x[-2]
    if pd.isnull(price) == True:
        price = x[-3]
    if pd.isnull(price) == True:
        price = x[-4]
    print(name, price)
    items = [name, price]
    final_data.append(items)

df = pd.DataFrame(final_data, columns=['Name', 'price'])
df.to_excel('prices.xlsx', index=True)