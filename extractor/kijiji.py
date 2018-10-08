import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.kijiji.ca/v-classic-cars/edmonton/1966-chevrolet-corvair-fully-restored/1351160283?enableSearchNavigationFlag=true")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

price = soup.find(class_="currentPrice-3131760660").get_text()
print(price)

title = soup.title.get_text().split("|")[0]
print(title)

description = soup.find(class_="descriptionContainer-3246526397").get_text().split("Description")[-1].strip().replace('\n','')
print(description)

tabela = soup.find_all(class_="itemAttribute-2841032265")

for item in tabela:
    if(item.get_text().count("Fuel") > 0 ):
        fuel = item.get_text().split("Type")[-1].strip().replace('\n','')
    elif(item.get_text().count("Transmission") > 0 ):
        transmission = item.get_text().split("Transmission")[-1].strip().replace('\n','')
    elif(item.get_text().count("Colour") > 0 ):
        exterior_color = item.get_text().split("Colour")[-1].strip().replace('\n','')
    elif(item.get_text().count("Kilometers") > 0 ):
        mileage = item.get_text().split("Kilometers")[-1].strip().replace('\n','')
print(fuel)
print(transmission)
print(exterior_color)
print(mileage)
'''
price
fuel
exterior_color
transmission
url
title
description
'''