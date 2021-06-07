import json
import ast
from typing import final
from openpyxl import load_workbook
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)
dataframe1 = pd.read_excel('delivery_rest_zomato.xlsx')
dictio = dataframe1.to_dict()
data = dictio['data']
datas = []
names = []
for x in range(1377):
    item = data[x]
    res = ast.literal_eval(item)
    datas.append(res)
    name = res['name']
    names.append(name)

dataframe2 = pd.read_excel('delivery_rest_zomato_urls.xlsx')
dictio2 = dataframe2.to_dict()
names2 = dictio2['Name']
final_names = []
for x in range(910):
    name = names2[x]
    final_names.append(name)

for x in final_names:
    if x in names:
        names.remove(x)

names_to_add = names
all_data = datas
data_to_add = []

for x in names_to_add:
    for y in all_data:
        listofitems = y.values()
        if x in listofitems:
            data_to_add.append(y)

values_list = []
for x in data_to_add:
    values = x.values()
    values_list.append(values)

final_data_to_add = []
for x in values_list:
    item = list(x)
    final_data_to_add.append(item)
print(final_data_to_add)

df = pd.DataFrame(final_data_to_add, columns = ['Name', 'Url', 'Cuisine', 'Price', 'Rating', 'New', 'Reviews'])
df.to_excel('extra_data.xlsx', index = True)