import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.kijiji.ca/v-cars-trucks/strathcona-county/2008-ford-ranger/1383323370")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

price = soup.find(class_="currentPrice-2872355490").get_text()

title = soup.title.get_text().split("|")[0]
#print(title)

description = soup.find(class_="descriptionContainer-2901313666").get_text().split("Description")[-1].strip().replace('\n','')
#print(description)

tabela = soup.find_all(class_="itemAttribute-2841032265")

for item in tabela:
    if(item.get_text().count("Fuel") > 0 ):
        fuel = item.get_text().split("Type")[-1].strip().replace('\n','')
    elif(item.get_text().count("Transmission") > 0 ):
        transmission = item.get_text().split("Transmission")[-1].strip().replace('\n','')
    elif(item.get_text().count("Colour") > 0 ):
        exterior_color = item.get_text().split("Colour")[-1].strip().replace('\n','')

#print(fuel)
#print(transmission)

'''
price
fuel
exterior_color
transmission
url
title
description
'''