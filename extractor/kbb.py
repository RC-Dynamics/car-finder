import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.kbb.com/cars-for-sale/494970912/?galleryview=photos")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.find(class_="primary-vehicle-title title-two ").get_text().strip().replace('\n','')

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

#vin = soup.find_all(class_= "paragraph-one vin")[0].get_text().split(":")[-1].strip().replace('\n','')

'''
price
fuel
exterior_color
interior_color
engine
transmission
url
title
'''