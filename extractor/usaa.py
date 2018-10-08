import requests
from bs4 import BeautifulSoup

page  = requests.get("https://usaa2.secure.zag.com/used-cars-for-sale/listing/KMHE24L18GA008696/2016-hyundai-sonata/")
print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')

tabela = soup.find_all(class_="heading-5 text-truncate")
for item in tabela:
    if(item.get_text().split()[0] == "Exterior"):
        exterior_color = item.get_text().split("Color")[-1].strip()
    if(item.get_text().split()[0] == "Interior"):
        interior_color = item.get_text().split("Color")[-1].strip()
    if(item.get_text().split()[0] == "Transmission"):
        transmission = item.get_text().split()[-1].strip()
    if(item.get_text().split()[0] == "Fuel"):
        fuel = item.get_text().split("Type")[-1].strip()
    if(item.get_text().split()[0] == "Engine"):
        engine = item.get_text().split("Engine")[-1].strip()
    if(item.get_text().split()[0] == "Mileage"):
        mileage = item.get_text().split("Mileage")[-1].strip()

title = soup.title.get_text().split('|')[0]


price_list = soup.find(class_="spacing-2 col-12 col-md-5 col-lg-4")

for item in price_list.descendants:
    try:
        if(item.get_text().split("dvertised")[0].strip() == "Price DetailsA" ):
          price = item.get_text().split("ised Price")[-1].strip()
    except:
        pass

print(title)
print(price)
print(exterior_color)
print(interior_color)
print(engine)
print(fuel)
print(mileage)
print(transmission)