import requests
from bs4 import BeautifulSoup
import re

page  = requests.get("https://www.marblesautomotive.com/inventory/2015/Chevrolet/Equinox/NY/Penn%20Yan/1GNFLFEK2FZ129044/")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.find_all(class_="inventory-main-line")[0].get_text().strip().replace('\n','')

tabela = soup.find(id="vehicle-info-wrapper")

for child in tabela.descendants:
            
            try:
                if(child.get_text().split()[0] == "Exterior:" and child.get_text().split(":")[-1] != " "):
                    exterior_color = child.get_text().split(":")[-1].strip()
                if(child.get_text().split()[0] == "Interior:" and child.get_text().split(":")[-1] != " "):
                    interior_color = child.get_text().split(":")[-1].strip()
                if(child.get_text().split()[0] == "Engine:" and child.get_text().split(":")[-1] != " "):
                    engine = child.get_text().split(":")[-1].strip()
                if(child.get_text().split()[0] == "Transmission:" and child.get_text().split(":")[-1] != " "):
                    transmission = child.get_text().split(":")[-1].strip()
            
            except AttributeError:
                pass

price_tree = soup.find(class_="inventory-price")

for child in price_tree.descendants:
            
            try:
                if(child.get_text().split()[0] == "Price:" and child.get_text().split(":")[-1] != " "):
                    price = child.get_text().split(":")[-1].strip()
            except:
                pass

description_list =[]
description_tree = soup.find(id="vehicle-detail-options")
#print(description_tree)
for child in description_tree.descendants:
    try:
       description_list.append(child.get_text()) 
    except:
        pass


description_list.pop(0)

description = ""

for i in range(len(description_list)):
    if (i == 0):
        description = description + description_list[i]
    else: 
        description = description + '\n' + description_list[i]

'''
description
price
exterior_color
interior_color
transmission
engine
title
'''