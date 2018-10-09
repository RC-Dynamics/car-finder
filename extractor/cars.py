import requests
from bs4 import BeautifulSoup
import json

page  = requests.get("https://www.cars.com/vehicledetail/detail/747061720/overview/")
print(page.status_code)


price=""
exterior_color=""
interior_color=""
transmission=""
engine=""
title=""

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.title.get_text().split("|")[0]

price_class = soup.find_all(class_="vehicle-info__price-display vehicle-info__price-display--dealer cui-heading-2")
price = price_class[0].get_text()

tabela = soup.find_all(class_="vdp-details-basics__item")
for item in tabela:
    if(item.get_text().split()[0] == "Fuel"):
        fuel = item.get_text().split(":")[-1]
        fuel = fuel.strip().replace('\n','')
    elif(item.get_text().split()[0] == "Exterior"):
        exterior_color = item.get_text().split(":")[-1]
        exterior_color = exterior_color.strip().replace('\n','')
    elif(item.get_text().split()[0] == "Interior"):
        interior_color = item.get_text().split(":")[-1]
        interior_color = interior_color.strip().replace('\n','')
    elif(item.get_text().split()[0] == "Engine:"):
        engine = item.get_text().split(":")[-1]
        engine = engine.strip().replace('\n','')
    elif(item.get_text().split()[0] == "Transmission:"):
        transmission = item.get_text().split(":")[-1]
        transmission = transmission.strip().replace('\n','')
    elif(item.get_text().split()[0] == "Mileage:"):
        mileage = item.get_text().split(":")[-1]
        mileage = mileage.strip().replace('\n','')


data = {
    'Title': title,
    'Price': price,
    'Exterior Color' : exterior_color,
    'Interior Color' : interior_color,
    'Engine' : engine,
    'Fuel' : fuel,
    'Mileage' : mileage,
    'Transmission': transmission
    }

with open('cars.txt', 'w') as outfile:  
    json.dump(data, outfile)


#print(title)
#print(price)
#print(exterior_color)
#print(interior_color)
#print(engine)
#print(fuel)
#print(mileage)
#print(transmission)