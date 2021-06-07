import openpyxl
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import pandas as pd

workbook = openpyxl.load_workbook('urls.xlsx')
sheet = workbook.active
urls = []
for x in sheet['B']:
    url = x.value
    urls.append(url)
urls.remove('url')
final_urls = []
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
for x in urls:
    page = requests.get(x, headers=headers)
    content = page.content
    print(f"Working url: {x}")
    soup = BeautifulSoup(content, 'html.parser')
    for parent in soup.find_all(class_="jumbo-tracker"):
        a_tag = parent.find("a")
        base = "https://www.zomato.com/jaipur/dine-out"
        link = a_tag.attrs['href']
        url = urljoin(base,link)
        print(url)
        final_urls.append(url)
    print()

df = pd.DataFrame(final_urls, columns=["Urls"])
df.to_excel('final_urls.xlsx', index=True)