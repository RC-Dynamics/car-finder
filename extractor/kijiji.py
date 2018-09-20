import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.kijiji.ca/v-cars-trucks/strathcona-county/2014-dodge-grand-caravan-sxt-in-excellent-condition/1384140248?enableSearchNavigationFlag=true")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

tabela = soup.find_all(class_="itemAttribute-2841032265")

str1 = "vamos la pracasa cara"
str2 = str1.count("pra")
print(str2)

#for item in tabela:
    #print(item.get_text())