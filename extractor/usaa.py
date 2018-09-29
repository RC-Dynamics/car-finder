import requests
from bs4 import BeautifulSoup

page  = requests.get("https://www.marblesautomotive.com/inventory/2015/Chrysler/Town%20%26%20Country/NY/Penn%20Yan/2C4RC1BG9FR637515/")
print(page.status_code)
