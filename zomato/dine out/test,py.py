import openpyxl
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import requests
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
workbook = openpyxl.load_workbook('urls.xlsx')
sheet = workbook.active
urls = []
for x in sheet['B']:
    url = x.value
    urls.append(url)
urls.remove('url')
data = []
for x in urls:
    page = requests.get(x, headers=headers)
    content = page.content

    print(f'Working Url: {x}')
    print()
    class_name = ""
    soup = BeautifulSoup(content, 'html.parser')
    for parent in soup.find_all(class_='sc-1mo3ldo-0'):
        jumbo = parent.find(class_='jumbo-tracker')
        if jumbo != None:
            classes = jumbo.find_all('a')
            classes1 = classes[1]
            classesname = classes1.attrs['class']
            class_name = " ".join(classesname)
    print(class_name)
    items = []
    for parent in soup.find_all(class_=class_name):
        p = parent.find_all('p')
        for x in p:
            print(x.get_text())
            items.append(x.get_text())
        data.append(items)
        items=[]
        print()
print(data)
df = pd.DataFrame(data)
df.to_excel('prices.xlsx', index=False)