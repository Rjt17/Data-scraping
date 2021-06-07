from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import openpyxl
 
# Give the location of the file
 
urls = []
workbook = openpyxl.load_workbook('href2.xlsx')
sheet = workbook.active
for x in sheet['A']:
    div = x.value
    soup = BeautifulSoup(div, "html.parser")
    for parent in soup.find_all("a"):
        link = parent.attrs['href']
        base = "https://www.zomato.com/jaipur/restaurants/"
        url = urljoin(base, link)
        urls.append(url)

df = pd.DataFrame(urls, columns=['url'])
df.to_excel('urls2.xlsx', index=True)