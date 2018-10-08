import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.buyacar.co.uk/bmw/3-series/3-series-saloon/330d-m-sport-4dr-step-auto-70258/deal-1444890")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.title.get_text().split('|')[0]

price = soup.find(class_="finance-info-price").get_text()

tabela = soup.find(class_="about-vehicle-wrapper")
for item in tabela.descendants:
    try:
        if(item.get_text().split(":")[0] == "Gearbox"):
            transmission = item.get_text().split(":")[-1].strip()
        if(item.get_text().split(":")[0] == "Colour"):
            exterior_color = item.get_text().split(":")[-1].strip()
        if(item.get_text().split(":")[0] == "Fuel"):
            fuel = item.get_text().split(":")[-1].strip()
        if(item.get_text().split(":")[0] == "Mileage"):
            mileage = item.get_text().split(":")[-1].strip()
    except:
        pass

description_list =soup.find(class_="detail")
description = ""
_pass = False
for item in description_list:
    try:
        if(_pass):
            description = description + '\n' +item.get_text()
        else:
            description = description  +item.get_text()
            _pass = True
    except:
        pass

print(price)
print(description)
print(title)
print(transmission)
print(exterior_color)
print(fuel)
print(mileage)