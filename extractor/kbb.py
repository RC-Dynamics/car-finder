import requests
from bs4 import BeautifulSoup
import json

page  = requests.get("https://www.kbb.com/cars-for-sale/494970912/?galleryview=photos")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.title.get_text().split('|')[0]

price = soup.find(class_="price").get_text().strip().replace('\n','')

tabela_class = soup.find_all(class_="details-list")[0].get_text()
tabela = tabela_class.split("\n")

tabela = filter(None, tabela)

for item in tabela:
    if(item.split()[0] == "Fuel"):
        fuel = item.split(":")[-1].strip().replace('\n','')
    elif(item.split()[0] == "Exterior"):
        exterior_color = item.split(":")[-1].strip().replace('\n','')
    elif(item.split()[0] == "Interior"):
        interior_color = item.split(":")[-1].strip().replace('\n','')
    elif(item.split()[0] == "Engine:"):
        engine = item.split(":")[-1].strip().replace('\n','')
    elif(item.split()[0] == "Transmission:"):
        transmission = item.split(":")[-1].strip().replace('\n','')
    elif(item.split()[0] == "Mileage:"):
        mileage = item.split(":")[-1].strip().replace('\n','')


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

with open('kbb.txt', 'w') as outfile:  
    json.dump(data, outfile)

#print(title)
#print(price)
#print(exterior_color)
#print(interior_color)
#print(engine)
#print(mileage)
#print(fuel)
#print(transmission)