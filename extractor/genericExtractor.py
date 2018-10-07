import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.usedcars.com/vehicle-details/234566104/?id=33378&prev=srp&zipcode=90006")
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
#walk(soup)
#print(mapList)

#print(maxKey(mapList))
body = BeautifulSoup(maxKey(mapList),"html.parser")

#print(body)
print(len(body))

for item in body.descendants:
    try:
       
        if item.get_text().split(":")[0].strip().replace('\n','') in ["Fuel","Fuel Type"] and ": " in item.text and len(item.text) < 30:
            print(item.text.strip())
    
        if item.get_text().split(":")[0].strip().replace('\n','') in ["Exterior","Exterior Color","Color","Colour"] and ": " in item.text and len(item.text) < 40 and item.get_text().split(":")[-1] != " ":
            print(item.get_text().strip())
        
    except:
        pass

#print(carData)
#NEED TO REPLACE SEARCH WORDS FROM THE DATA RESULT


'''
if item.get_text().split(":")[-1].strip().replace('/n','') in ["Gasoline","Diesel"] and "Fuel" not in item.text:
            print(item.text.strip())
'''

'''elif(item.get_text().split()[0] == "Exterior"):
            print(item.get_text()) '''#usaa

'''        elif(item.get_text().split(" Color")[0].strip().replace('\n','') == "Exterior"):
            print(item.get_text().strip().replace('\n',''))'''#usedcars            