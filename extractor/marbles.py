import requests
from bs4 import BeautifulSoup

description=""
price=""
exterior_color=""
interior_color=""
transmission=""
engine=""
title=""

def desc_options (description):
    description_list =[]
    for child in description_tree.descendants:
        try:
            description_list.append(child.get_text()) 
        except:
            pass

    description_list.pop(0)

    try:
        description_list.remove("Description")
    except:
        pass

    for i in range(len(description_list)):
        if (i == 0):
            description = description + description_list[i]
        else: 
            description = description + '\n' + description_list[i]
    return description


page  = requests.get("https://www.marblesautomotive.com/inventory/2015/Chrysler/Town%20%26%20Country/NY/Penn%20Yan/2C4RC1BG9FR637515/")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.find_all(class_="inventory-main-line")[0].get_text().strip().replace('\n','')

tabela = soup.find(id="vehicle-info-wrapper")

for child in tabela.descendants:
            
            try:
                if(child.get_text().split()[0] == "Exterior:" and child.get_text().split(":")[-1] != " "):
                    exterior_color = child.get_text().split(":")[-1].strip()
                if(child.get_text().split()[0] == "Interior:" and child.get_text().split(":")[-1] != " "):
                    interior_color = child.get_text().split(":")[-1].strip()
                if(child.get_text().split()[0] == "Engine:" and child.get_text().split(":")[-1] != " "):
                    engine = child.get_text().split(":")[-1].strip()
                if(child.get_text().split()[0] == "Transmission:" and child.get_text().split(":")[-1] != " "):
                    transmission = child.get_text().split(":")[-1].strip()
                if(child.get_text().split()[0] == "Odometer:" and child.get_text().split(":")[-1] != " "):
                    mileage = child.get_text().split(":")[-1].strip()    
                    
            
            except AttributeError:
                pass

price_tree = soup.find(class_="inventory-price")

for child in price_tree.descendants:
            
            try:
                if(child.get_text().split()[0] == "Price:" and child.get_text().split(":")[-1] != " "):
                    price = child.get_text().split(":")[-1].strip()
            except:
                pass


description = ""
try: 
    description_tree = soup.find(id="vehicle-detail-options")
    description = desc_options(description)
except:
    pass
try:
    description_tree = soup.find(id="vehicle-detail-desc")
    #print(description_tree)
    for item in description_tree:
        if(description == ""):
            try:
                description = description + item.get_text()
            except:
                description = description_tree.get_text()
                break
        else:
            description = description + '\n' +item.get_text()
except:
    pass
    
print(description)
print(price)
print(exterior_color)
print(interior_color)
print(transmission)
print(engine)
print(title)
print(mileage)