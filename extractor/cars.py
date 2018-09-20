import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.cars.com/vehicledetail/detail/747061720/overview/")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.title.get_text().split("For Sale")[0]
print(title)

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