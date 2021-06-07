from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import requests
import openpyxl

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

workbook = openpyxl.load_workbook('swiggy_rests.xlsx')
sheet = workbook.active
urls = []
for x in sheet['C']:
    urls.append(x.value)
urls.remove('Url')
length = len(urls)
i = 1
data = []
offers = []
for url in urls:
    page = requests.get(url, headers=headers)
    content = page.content
    print(f'Working Url: {url} | {i}/{length}')
    i+=1

    soup = BeautifulSoup(content, "html.parser")
    found = soup.find_all(class_='_3lvLZ')
    if found == []:
        item = [url, "None"]
        data.append(item)
        continue
    for parent in found:
        offer = parent.get_text()
        offers.append(offer)
        item = [url, offers]
        offers = []
    data.append(item)
df = pd.DataFrame(data, columns=['Url', 'Offers'])
df.to_excel('offers.xlsx', index=True)