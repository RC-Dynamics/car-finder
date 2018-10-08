import requests
from bs4 import BeautifulSoup

description=""
price=""
exterior_color=""
interior_color=""
transmission=""
engine=""
title=""

page  = requests.get("https://www.marblesautomotive.com/inventory/2015/Chrysler/Town%20%26%20Country/NY/Penn%20Yan/2C4RC1BG9FR637515/")
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
                if(child.get_text().split()[0] == "Odometer:" and child.get_text().split(":")[-1] != " "):
                    mileage = child.get_text().split(":")[-1].strip()    
                    
            
            except AttributeError:
                pass

price_tree = soup.find(class_="inventory-price")

for child in price_tree.descendants:
            
            try:
                if(child.get_text().split()[0] == "Price:" and child.get_text().split(":")[-1] != " "):
                    price = child.get_text().split(":")[-1].strip()
            except:
                pass

print(title)
print(price)
print(exterior_color)
print(interior_color)
print(engine)
print(mileage)
print(transmission)