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
        transmission=""
        title=""


        try:
            soup = BeautifulSoup(page.content, 'html.parser')

            try:
                price = soup.find(class_="currentPrice-441857624").get_text()
            except:
                print("Price not extracted")
            
            try:
                title = soup.title.get_text().split("|")[0]
            except:
                print("Title not extracted")

            try:
                tabela = soup.find_all(class_="itemAttribute-983037059")

                for item in tabela:
                    if(item.get_text().count("Fuel") > 0 ):
                        fuel = item.get_text().split("Type")[-1].strip().replace('\n','')
                    elif(item.get_text().count("Transmission") > 0 ):
                        transmission = item.get_text().split("Transmission")[-1].strip().replace('\n','')
                    elif(item.get_text().count("Colour") > 0 ):
                        exterior_color = item.get_text().split("Colour")[-1].strip().replace('\n','')
                    elif(item.get_text().count("Kilometers") > 0 ):
                        mileage = item.get_text().split("Kilometers")[-1].strip().replace('\n','')
            except:
                print("Tabel not extracted")

            data = {
                'Title': title,
                'Price': price,
                'Colour' : exterior_color,
                'Kilometers' : mileage,
                'Transmission': transmission
                }
            tools.write_json("kijiji", id, data)    
            print(title)
            print(price)
            print(exterior_color)
            print(fuel)
            print(mileage)
            print(transmission)
        
        except:
            print("Page not downloaded")
    else:
        print("Page request error")


url = "https://www.kijiji.ca/v-classic-cars/strathcona-county/camaro-iroc-z/1100186238?enableSearchNavigationFlag=true"
extrator(url, "7")