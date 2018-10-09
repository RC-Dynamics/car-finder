from bs4 import BeautifulSoup
from selenium import webdriver
import signal
import json

driver = webdriver.PhantomJS()
driver.get("https://shift.com/car/c179628")
page = BeautifulSoup(driver.page_source, "html.parser")
driver.service.process.send_signal(signal.SIGTERM)

fuel=""
price=""
exterior_color=""
interior_color=""
transmission=""
engine=""
title=""


price = page.find(class_="CarProfileDetails__pricing-item-value").get_text()

title = page.title.get_text().split("|")[0]

tabela = page.find(class_="CarProfileDetails__specs-items")

for item in tabela:
        if(item.get_text().split("rior")[0] == "Exte"):
            exterior_color = item.get_text().split("Exterior")[-1].strip().replace('\n','')
        if(item.get_text().split("rior")[0] == "Inte"):
            interior_color = item.get_text().split("Interior")[-1].strip().replace('\n','')
        if(item.get_text().split(" type")[0] == "Fuel"):
            fuel = item.get_text().split("type")[-1].strip().replace('\n','')

specs = page.find(class_="CarProfileDetails__overview-items")


for item in specs.descendants:
    try:    
        if(item.get_text().strip() == "Manual" or item.get_text().strip() == "Automatic"):
            transmission = item.get_text().strip().replace('\n','')
        if(item.get_text().find("AWD",0,4) == 0 or item.get_text().find("FWD",0,4) == 0 or item.get_text().find("RWD",0,4) == 0):
            engine = item.get_text().strip().replace('\n','')
        
    except:
        pass


data = {
    'Title': title,
    'Price': price,
    'Exterior Color' : exterior_color,
    'Interior Color' : interior_color,
    'Engine' : engine,
    'Fuel' : fuel,
    'Transmission': transmission
    }

with open('shift2.txt', 'w') as outfile:  
    json.dump(data, outfile)


print(title)
print(price)
print(exterior_color)
print(interior_color)
print(fuel)
print(engine)
print(transmission)