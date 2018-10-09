import requests
from bs4 import BeautifulSoup
import json

page  = requests.get("https://www.usedcars.com/vehicle-details/246240533/?id=33378&prev=srp&zipcode=90006")
print(page.status_code)

mileage = ""
price=""
exterior_color=""
interior_color=""
transmission=""
engine=""
title=""

soup = BeautifulSoup(page.content, 'html.parser')

tabela = soup.find(class_="ucc-table ucc-table--summary")

title = soup.title.get_text()

for child in tabela:
    try:
        if(child.get_text().split("$")[0].strip().replace('\n','') == "Price"):
            price = child.get_text().split("Price")[-1].strip().replace('\n','')
        if(child.get_text().split(" Color")[0].strip().replace('\n','') == "Exterior"):
            exterior_color = child.get_text().split("Color")[-1].strip().replace('\n','')
        if(child.get_text().split(" Color")[0].strip().replace('\n','') == "Interior"):
            interior_color = child.get_text().split("Color")[-1].strip().replace('\n','')
        if(child.get_text().split("gine")[0].strip().replace('\n','') == "En"):
            engine = child.get_text().split("Engine")[-1].strip().replace('\n','')
        if(child.get_text().split("mission")[0].strip().replace('\n','') == "Trans"):
            transmission = child.get_text().split("Transmission")[-1].strip().replace('\n','')
        if(child.get_text().split("age")[0].strip().replace('\n','') == "Mile"):
            mileage = child.get_text().split("Mileage")[-1].strip().replace('\n','')
    except:
        pass

data = {
    'Title': title,
    'Price': price,
    'Exterior Color' : exterior_color,
    'Interior Color' : interior_color,
    'Engine' : engine,
    'Mileage' : mileage,
    'Transmission': transmission
    }

with open('usedcars.txt', 'w') as outfile:  
    json.dump(data, outfile)


print(title)
print(price)
print(exterior_color)
print(interior_color)
print(engine)
print(mileage)
print(transmission)