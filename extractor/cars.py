import requests
from bs4 import BeautifulSoup
import json
import tools

def extrator(url, id):

    page  = requests.get(url)
    print(page.status_code)

    fuel=""
    mileage = ""
    price=""
    exterior_color=""
    interior_color=""
    transmission=""
    engine=""
    title=""

    try:
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            title = soup.title.get_text().split("|")[0]
        except:
            print("Title not extracted")

        try:
            price_class = soup.find_all(class_="vehicle-info__price-display vehicle-info__price-display--dealer cui-heading-2")
            price = price_class[0].get_text()
        except:
            print("Price not extracted")
        try:
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
                elif(item.get_text().split()[0] == "Mileage:"):
                    mileage = item.get_text().split(":")[-1]
                    mileage = mileage.strip().replace('\n','')
        except:
            print("Table not extracted")

    
    except:
        print("Page not downloaded")

    tools.write_json("cars", id,mileage, exterior_color, price, transmission, title)

    print(title)
    print(price)
    print(exterior_color)
    print(interior_color)
    print(engine)
    print(fuel)
    print(mileage)
    print(transmission)

url = "https://www.cars.com/vehicledetail/detail/746781127/overview/"
extrator(url, "5")