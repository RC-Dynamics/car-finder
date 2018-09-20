import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.kijiji.ca/v-cars-trucks/strathcona-county/2008-ford-ranger/1383323370")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

tabela = soup.find_all(class_="itemAttribute-2841032265")

'''str1 = "vamos la pracasa cara"
str2 = str1.find("pra")
print(str2)'''



for item in tabela:
    if(item.get_text().count("Fuel") > 0 ):
        fuel = item.get_text().split("Type")[-1].strip().replace('\n','')
    elif(item.get_text().count("Fuel") > 0 ):
        fuel = item.get_text().split("Type")[-1].strip().replace('\n','')

print(fuel)