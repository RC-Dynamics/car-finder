import requests
from bs4 import BeautifulSoup
import json
import tools

def extrator(site, id):

        mileage =""
        price=""
        exterior_color=""
        transmission=""
        title=""
        fuel=""

        page  = requests.get(site)
        
        print(page.status_code)
        if (page.status_code == 200):
            try: 
                soup = BeautifulSoup(page.content, 'html.parser')

                try:
                    title = soup.title.get_text().split('|')[0]
                except:
                    print("Title not extracted")

                try:
                    price = soup.find(class_="finance-info-price").get_text()
                except:
                    print("Price not extracted")
                try:    
                    tabela = soup.find(class_="about-vehicle-wrapper")
                    for item in tabela.descendants:
                        try:
                            if(item.get_text().split(":")[0] == "Gearbox"):
                                transmission = item.get_text().split(":")[-1].strip()
                            if(item.get_text().split(":")[0] == "Colour"):
                                exterior_color = item.get_text().split(":")[-1].strip()
                            if(item.get_text().split(":")[0] == "Fuel"):
                                fuel = item.get_text().split(":")[-1].strip()
                            if(item.get_text().split(":")[0] == "Mileage"):
                                mileage = item.get_text().split(":")[-1].strip()
                        except:
                            pass
                except:
                    print("Table with transmission, exterior color, fuel and mileage not founded")
                data = {
                    'Title': title,
                    'Price': price,
                    'Exterior Color' : exterior_color,
                    'Mileage' : mileage,
                    'Transmission': transmission
                }
                tools.write_json("extract", id, data)
            except:
                print("Page not downloaded")
        else:
            print("Page request error")