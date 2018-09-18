import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.kbb.com/cars-for-sale/493323709/?galleryview=photos")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

tabela_text = soup.find_all(class_="details-list")[0].get_text()
tabela = tabela_text.split("\n")

for item in tabela:
    print(item)