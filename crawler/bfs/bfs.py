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
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    MAX_VISITS = 1
    debug = False

    def __init__(self, site, dbg=False):
        self.url = site['site']
        self.order.append('')
        self.disallow = site['disallow']
        self.debug = dbg

    def check_allow(self, path):
        return (path in self.disallow)

    def bfs_visit(self):
        visit_quantity = 0
        if (self.debug):
            out = open('debug_links/' + self.url.split('www.')[1].split('/')[0] + '.txt', 'w')
        while visit_quantity < self.MAX_VISITS:
            print (self.url)
            html = requests.get(self.url + self.order.pop(0), headers=self.headers)
            soup = BeautifulSoup(html.text, 'html.parser')
            out.write(html.text)
            out.write('\n\n')
            links = soup.find_all('a', href=True)
            for l in links:
                if (self.debug):
                    out.write(l['href'])
                    out.write('\n')
            visit_quantity += 1
            # time.sleep(1)
        
        if (self.debug):
            out.close()

if (__name__ == "__main__"):
    p = PreProcessing("../../site.txt")
    sites = p.get_sites_info()
    for s in sites:
        c = CrawlerBFS(s, True)
        c.bfs_visit()