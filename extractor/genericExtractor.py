import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.buyacar.co.uk/bmw/3-series/3-series-saloon/330d-m-sport-4dr-step-auto-70258/deal-1444890")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

mapList = {}

def check(mapList, real_key):
    for key in mapList:
        if key == real_key:
            return True
    return False


def walk(soup):
    if soup.name is not None:    
        for child in soup.children:
            if soup.name in ["p","h2","h3","h4","pre","br","div"]:
                if check(mapList, str(child.parent)):
                    mapList[str(child.parent)] = 1 + mapList[(str(child.parent))]
                else:
                    mapList[str(child.parent)] = 1
            walk(child)

def maxKey(mapList):
    maxK = ""
    maxV = 0
    for key in mapList:
        if maxV < mapList[key]:
            maxV = mapList[key]
            maxK = key
    return maxK

walk(soup)
#print(mapList)

#print(maxKey(mapList))
body = BeautifulSoup(maxKey(mapList),"html.parser")

#print(body)
print(len(body))
for item in body.descendants:
    try:
        
        if "Fuel:" in item:
            print(item)
            #print("\n\n\n")
    except:
        pass