import requests
import time
from bs4 import BeautifulSoup
import sys
sys.path.append('../shared')

from pre_processing import PreProcessing

class CrawlerBFS:
    url = ''
    order = []
    disallow = []
    MAX_VISITS = 1

    def __init__(self, site):
        self.url = site['site']
        self.order.append('')
        self.disallow = site['disallow']

    def check_allow(self, path):
        return (path in self.disallow)

    def bfs_visit(self):
        visit_quantity = 0
        while visit_quantity < self.MAX_VISITS:
            html = requests.get(self.url + self.order.pop(0))
            soup = BeautifulSoup(html.text, 'html.parser')
            links = soup.find_all('a', href=True)
            for l in links:
                print (l['href'])
                print ('\n\n')
            time.sleep(1)
            visit_quantity += 1

if (__name__ == "__main__"):
    p = PreProcessing("../../site.txt")
    sites = p.get_sites_info()
    for s in sites:
        c = CrawlerBFS(s)
        c.bfs_visit()
        break