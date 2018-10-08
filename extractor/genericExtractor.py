import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.usedcars.com/vehicle-details/246240533/?id=33378&prev=srp&zipcode=90006")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')
#print(soup)
mapList = {}

def check(mapList, real_key):
    for key in mapList:
        if key == real_key:
            return True
    return False


def walker(soup):
    if soup.name is not None:
        for child in soup.children:
            count = 0
            if "Fuel" in child.encode('utf-8'):
                count += 1
            if "Transmission" in child.encode('utf-8'):
                count += 1
            if "Exterior" in child.encode('utf-8'):
                count += 1
            if "Interior" in child.encode('utf-8'):
                count += 1
            if "Description" in child.encode('utf-8'):
                count += 1
            if "Price" in child.encode('utf-8'):
                count += 1
            if "$" in child.encode('utf-8'):
                count += 1
            if "Engine" in child.encode('utf-8'):
                count += 1

            if check(mapList, str(child.parent)):
                mapList[str(child.parent)] = count + mapList[str(child.parent)]
            else:
                mapList[str(child.parent)] = count
            walker(child)

def maxKey(mapList):
    maxK = ""
    maxV = 0
    for key in mapList:
        if maxV < mapList[key]:
            maxV = mapList[key]
            maxK = key
    return maxK

def refine(tree):
    carData = None
    try:
        for item in tree.descendants:
            if(item.get_text().split()[0] == "Fuel"):
                carData = item.get_text().split(":")[-1].strip().replace('\n','')
                print(carData)    
    except:
        pass

    return carData

walker(soup)

price = ''
exterior = ''
interior = ''
engine = ''
transmission = ''
mileage = ''
fuel = ''

#walk(soup)
#print(mapList)

#print(maxKey(mapList))
body = BeautifulSoup(maxKey(mapList),"html.parser")

#print(body)
print(len(body))

title = soup.title.get_text().split('|')[0]
print(title)

catch_price = True
catch_exterior = True
catch_interior = True
catch_engine = True
catch_transmission = True
catch_mileage = True
catch_fuel = True



for item in body.descendants:
    try:
        if u'\u00A3' in item and ',' in item:
            if catch_price:
                price = item
                catch_price = False
    
        elif soup.find(class_="price") is not None and catch_price:
            price = soup.find(class_="price").get_text().strip().replace('\n','')
            catch_price = False
        
        elif '$' in item.text and ',' in item.get_text() and len(item.get_text().strip()) < 10:
            if catch_price:
                item.text.strip()
                catch_price = False
        
        if item.get_text().split(":")[0].strip().replace('\n','') in ["Fuel","Fuel Type"] and ": " in item.text and len(item.text) < 30:
            if catch_fuel:
                fuel = item.get_text().strip().replace('\n','')
                catch_fuel = False

        elif "Fuel" in item.get_text().strip().replace('\n','')  and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            if catch_fuel:
                fuel = item.get_text().strip().replace('\n','')
                catch_fuel = False

        if item.get_text().split(":")[0].strip().replace('\n','') in ["Exterior","Exterior Color","Color","Colour"] and ": " in item.text and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            if catch_exterior:
                exterior_color = item.get_text().strip()
                catch_exterior = False

        elif "Exterior" in item.get_text().strip().replace('\n','')  and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            if catch_exterior:
                exterior_color = item.get_text().strip().replace('\n','')
                catch_exterior = False

        elif "Colour" in item.get_text().strip().replace('\n','')  and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            if catch_exterior:
                exterio_color = item.get_text().strip().replace('\n','')    
                catch_exterior = False
        
        if item.get_text().split(":")[0].strip().replace('\n','') in ["Gearbox","Transmission"] and ": " in item.text and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            print(item.get_text().strip())

        elif "Transmission" in item.get_text().strip().replace('\n','')  and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            if catch_transmission:
                transmission = item.get_text().strip().replace('\n','')
                catch_transmission = False

        if item.get_text().split(":")[0].strip().replace('\n','') in ["Interior Color", "Interior"] and ": " in item.text and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            if catch_interior:
                interior_color = item.get_text().strip().replace('\n','')
                catch_interior = False

        elif "Interior" in item.get_text().strip().replace('\n','')  and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            if catch_interior:
                interior_color = item.get_text().strip().replace('\n','')
                catch_interior = False

        if item.get_text().split(":")[0].strip().replace('\n','') in ["Engine"] and ": " in item.text and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            if catch_engine:
                engine = item.get_text().strip().replace('\n','')
                catch_engine = False

        elif "Engine" in item.get_text().strip().replace('\n','')  and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            if catch_engine:
                engine = item.get_text().strip().replace('\n','')
                catch_engine = False

        if item.get_text().split(":")[0].strip().replace('\n','') in ["Mileage","Odometer","Kilometers"] and ": " in item.text and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            if catch_mileage:
                mileage = item.get_text().strip().replace('\n','')
                catch_mileage = False

        elif "Mileage" in item.get_text().strip().replace('\n','')  and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            if catch_mileage:
                mileage = item.get_text().strip().replace('\n','')
                catch_mileage = False
        
    
    except:
        pass

print(exterior_color)
print(interior_color)
print(engine)
print(fuel)
print(mileage)
print(transmission)
#print(carData)
#NEED TO REPLACE SEARCH WORDS FROM THE DATA RESULT
#Title from marbles

'''
if item.get_text().split(":")[-1].strip().replace('/n','') in ["Gasoline","Diesel"] and "Fuel" not in item.text:
            print(item.text.strip())
'''

'''elif(item.get_text().split()[0] == "Exterior"):
            print(item.get_text()) '''#usaa

'''        elif(item.get_text().split(" Color")[0].strip().replace('\n','') == "Exterior"):
            print(item.get_text().strip().replace('\n',''))'''#usedcars            