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
        interior_color=""
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
                tabela = soup.find(class_="ucc-table ucc-table--summary")

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
                        if(child.get_text().split("age")[0].strip().replace('\n','') == "Mile"):
                            mileage = child.get_text().split("Mileage")[-1].strip().replace('\n','')
                    except:
                        pass
            except:
                print("Table not extracted")
                
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

url = "https://www.usedcars.com/vehicle-details/252238050/?id=33378&prev=srp&zipcode=90006"
extrator(url, "10")