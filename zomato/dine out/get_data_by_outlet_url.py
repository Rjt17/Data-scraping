import openpyxl
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import requests
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

workbook = openpyxl.load_workbook('final_urls.xlsx')
sheet = workbook.active
urls = []
for x in sheet['B']:
    url = x.value
    urls.append(url)
urls.remove('Urls')
i=1
length = 366
data = []
for y in urls:
    page = requests.get(y, headers=headers)
    content = page.content
    print(f'Working Url: {y} : {i}/386')
    i+=1
    soup = BeautifulSoup(content, 'html.parser')
    for parent in soup.find_all(class_='sc-giadOv tPcwa'):
        name = parent.find('h1', class_='sc-7kepeu-0 sc-cpmLhU iywipP')
        cuisine = parent.find(class_='sc-gFaPwZ kJabPi')
        a_tags = []
        for x in cuisine:
            a_tag = x.find(class_='sc-fhYwyz eYEQlP')
            a_tags.append(a_tag.get_text())
        cuisines = ", ".join(a_tags)
        rating = parent.find(class_='sc-1hez2tp-0 lhdg1m-2 bObnWx')
        no_reviews = parent.find(class_= 'sc-1hez2tp-0 lhdg1m-8 kMAHHC')
        url = y
        if name != None:
            name = name.get_text()
        else:
            name = "None"
        cuisines = cuisines
        if rating != None:
            rating = rating.get_text()
        else:
            rating = "None"
        if no_reviews != None:
            no_reviews = no_reviews.get_text()
        else:
            no_reviews = "None"
        item = [name, y, cuisines, rating, no_reviews]
        print(item)
        data.append(item)
print(data)
df = pd.DataFrame(data, columns=['Name', 'Url', 'Cuisine', 'Rating','Reviews'])
df.to_excel('prices_extra.xlsx', index = True)