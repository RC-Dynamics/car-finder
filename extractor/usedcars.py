import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.usedcars.com/vehicle-details/231537535/?id=33378&prev=srp&zipcode=90006")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

tabela = soup.find(class_="ucc-table ucc-table--summary")

title = soup.title.get_text()

description_list = soup.find( id="car-features")
description = ""
_pass = False
for item in description_list:
    try:
        if(item.get_text().strip() != "Car Features" and _pass):
            description = description + '\n' + item.get_text().strip().replace('\n\n',"")
        else:
            description = description + item.get_text().strip().replace('\n\n',"")
            _pass = True
    except:
        pass


for child in tabela:
    try:
        if(child.get_text().split("$")[0].strip().replace('\n','') == "Price"):
            price = child.get_text().split("Price")[-1].strip().replace('\n','')
        if(child.get_text().split(" Color")[0].strip().replace('\n','') == "Exterior"):
            exterior_color = child.get_text().split("Color")[-1].strip().replace('\n','')
        if(child.get_text().split(" Color")[0].strip().replace('\n','') == "Interior"):
            interior_color = child.get_text().split("Color")[-1].strip().replace('\n','')
        if(child.get_text().split("gine")[0].strip().replace('\n','') == "En"):
            engine = child.get_text().split("Engine")[-1].strip().replace('\n','')
        if(child.get_text().split("mission")[0].strip().replace('\n','') == "Trans"):
            transmission = child.get_text().split("Transmission")[-1].strip().replace('\n','')
    except:
        pass

#print(description)
#print(price)
#print(exterior_color)
#print(interior_color)
#print(engine)
#print(transmission)
#print(title)