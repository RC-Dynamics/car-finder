import requests
from bs4 import BeautifulSoup
import json

page  = requests.get("http://www.munstermanauto.com/vehicle/used-2013-volkswagen-beetle-coupe-25l-entry-hatchback-2d-3033001?refby=dealersite#ar_top")
print(page.status_code)

mileage = ""
price=""
exterior_color=""
transmission=""
engine=""
title=""

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.title.get_text()

tabela = soup.find_all(class_="ar_vehspec")

for item in tabela:
    if(item.get_text().split(" :")[0] == "Exterior"):
        exterior_color = item.get_text().split(" :")[-1].strip().replace('\n','')
    elif(item.get_text().split(" :")[0].strip() == "Sale Price"):
        price = item.get_text().split(" :")[-1].strip().replace('\n','')
    elif(item.get_text().split(" :")[0].strip() == "Transmission"):
        transmission = item.get_text().split(" :")[-1].strip().replace('\n','')
    elif(item.get_text().split(" :")[0].strip() == "Engine"):
        engine = item.get_text().split(" :")[-1].strip().replace('\n','')
    elif(item.get_text().split(" :")[0].strip() == "Mileage"):
        mileage = item.get_text().split(" :")[-1].strip().replace('\n','')


data = {
    'Title': title,
    'Price': price,
    'Exterior Color' : exterior_color,
    'Engine' : engine,
    'Mileage' : mileage,
    'Transmission': transmission
    }

with open('munstermanauto.txt', 'w') as outfile:  
    json.dump(data, outfile)


#print(title)
#print(price)
#print(exterior_color)
#print(engine)
#print(mileage)
#print(transmission)