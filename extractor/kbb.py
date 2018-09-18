import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.kbb.com/cars-for-sale/493323709/?galleryview=photos")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

tabela_class = soup.find_all(class_="details-list")[0].get_text()
tabela = tabela_class.split("\n")

tabela = filter(None, tabela)

for item in tabela:
    if(item.split()[0] == "Fuel"):
        fuel = item.split(":")[-1].strip().replace('\n','')
    if(item.split()[0] == "Exterior"):
        exterior_color = item.split(":")[-1].strip().replace('\n','')
    if(item.split()[0] == "Interior"):
        interior_color = item.split(":")[-1].strip().replace('\n','')
    if(item.split()[0] == "Engine:"):
        engine = item.split(":")[-1].strip().replace('\n','')

print(fuel, interior_color)
print(exterior_color)
print(engine)
'''
vin_class = soup.find_all(class_= "paragraph-one vin")[0].get_text()
vin = vin_class.'''