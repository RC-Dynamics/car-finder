from bs4 import BeautifulSoup
from selenium import webdriver
import signal

driver = webdriver.PhantomJS()
driver.get("https://shift.com/car/c152495")
page = BeautifulSoup(driver.page_source, "html.parser")
driver.service.process.send_signal(signal.SIGTERM)


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

description_tree = page.find(class_="CarProfileDetails__section CarProfileDetails__features")
description_list = []
description = ""
_pass = False
for item in description_tree.descendants:
    try:
        description_list.append(item.get_text())
    except:
        pass
description_list.pop(0)
description_list.pop(0)
description_list.pop(-1)
for item in description_list:
    if (_pass):
        description = description + '\n' + item
    else:
        description = description + item
        _pass = True

print(description)
#print(title)
#print(engine)
#print(transmission)
#print(exterior_color)
#print(interior_color)
#print(fuel)
#print(price)