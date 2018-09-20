import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=492946325&zip=90001&referrer=%2Fcars-for-sale%2Fsearchresults.xhtml%3Fzip%3D90001%26startYear%3D1981%26sortBy%3Drelevance%26vehicleStyleCodes%3DSEDAN%26incremental%3Dall%26firstRecord%3D0%26endYear%3D2019%26searchRadius%3D25&startYear=1981&numRecords=25&vehicleStyleCodes=SEDAN&firstRecord=0&endYear=2019&searchRadius=25")
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

tabela_class = soup.find_all(class_="col-xs-8 col-sm-9 col-md-10 col-lg-9")

print(tabela_class)

'''tabela = tabela_class.split("\n")

for item in tabela:
    print(item)'''