import requests
from bs4 import BeautifulSoup
import json
import tools

def extrator(url,id):
    page  = requests.get(url)
    print(page.status_code)

    if(page.status_code == 200):    
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
                title = soup.title.get_text().split('|')[0]
            except:
                print("Title not extracted")
            try:
                price = soup.find(class_="price").get_text().strip().replace('\n','')
            except:
                print("Price not extracted")

            try:
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
                    elif(item.split()[0] == "Mileage:"):
                        mileage = item.split(":")[-1].strip().replace('\n','')
            except:
                print("Table not extracted")

            data = {
                'Title': title,
                'Price': price,
                'Exterior Color' : exterior_color,
                'Mileage' : mileage,
                'Transmission': transmission
                }

            tools.write_json("kbb", id, data)

        except:
            print("Page not Downloaded")
        
        print(title)
        print(price)
        print(exterior_color)
        print(interior_color)
        print(engine)
        print(mileage)
        print(fuel)
        print(transmission)
    else:
        print("Page request error")
url = "https://www.kbb.com/cars-for-sale/494970912/?galleryview=photos"
extrator(url, "6")