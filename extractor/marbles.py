import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.marblesautomotive.com/inventory/2008/Cadillac/STS/NY/Penn%20Yan/1G6DA67V980199342/")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.find_all(class_="inventory-main-line")[0].get_text().strip().replace('\n','')

tabela = soup.find_all(id="vehicle-info-wrapper")

for item in tabela:
    print(item.get_text())
