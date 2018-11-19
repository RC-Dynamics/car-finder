import requests
from bs4 import BeautifulSoup
import json
import tools

def extrator(url,id):
    page  = requests.get(url)
    print(page.status_code)

    if(page.status_code == 200):
        price=""
        exterior_color=""
        interior_color=""
        transmission=""
        engine=""
        title=""
        
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            
            try:
                title = soup.find_all(class_="inventory-main-line")[0].get_text().strip().replace('\n','')
            except:
                print("Title not extracted")
            
            try:
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
            except:
                print("Table not extracted")

            try:
                price_tree = soup.find(class_="inventory-price")

                for child in price_tree.descendants:
                            
                            try:
                                if(child.get_text().split()[0] == "Price:" and child.get_text().split(":")[-1] != " "):
                                    price = child.get_text().split(":")[-1].strip()
                            except:
                                pass
            except:
                print("Price not extracted")

            data = {
                'Title': title,
                'Price': price,
                'Exterior Color' : exterior_color,
                'Mileage' : mileage,
                'Transmission': transmission
                }

            tools.write_json("extract", id, data)

            #print(title)
            #print(price)
            #print(exterior_color)
            #print(interior_color)
            #print(engine)
            #print(mileage)
            #print(transmission)

        except:
            print("Page not downloaded")
    else:
        print("Page request error")