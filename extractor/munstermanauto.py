import requests
from bs4 import BeautifulSoup
import json
import tools

def extrator(url, id):
    page  = requests.get(url)
    print(page.status_code)
    if(page.status_code == 200):
        mileage = ""
        price=""
        exterior_color=""
        transmission=""
        engine=""
        title=""

        try:
            soup = BeautifulSoup(page.content, 'html.parser')

            try:
                title = soup.title.get_text()
            except:
                print("Title not extracted")
            
            try:
                tabela = soup.find_all(class_="ar_vehspec")

                for item in tabela:
                    if(item.get_text().split(" :")[0] == "Exterior"):
                        exterior_color = item.get_text().split(" :")[-1].strip().replace('\n','')
                    elif(item.get_text().split(" :")[0].strip() == "Sale Price"):
                        price = item.get_text().split(" :")[-1].strip().replace('\n','')
                    elif(item.get_text().split(" :")[0].strip() == "Transmission"):
                        transmission = item.get_text().split(" :")[-1].strip().replace('\n','')
                    elif(item.get_text().split(" :")[0].strip() == "Engine"):
                        engine = item.get_text().split(" :")[-1].strip().replace('\n','')
                    elif(item.get_text().split(" :")[0].strip() == "Mileage"):
                        mileage = item.get_text().split(" :")[-1].strip().replace('\n','')
            except:
                print("Table not extracted")

            data = {
                'Title': title,
                'Price': price,
                'Exterior Color' : exterior_color,
                'Engine' : engine,
                'Mileage' : mileage,
                'Transmission': transmission
                }

            tools.write_json("extract", id, data)

            #print(title)
            #print(price)
            #print(exterior_color)
            #print(engine)
            #print(mileage)
            #print(transmission)
        
        except:
            print("Page not downloaded")
    
    else:
        print("Page request error")