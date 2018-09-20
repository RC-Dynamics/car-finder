import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.carsforsale.com/vehicle/details/47185039")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

tabela_class = soup.find_all(class_="vehicle-table")
print(tabela_class)