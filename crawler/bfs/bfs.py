import requests
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
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

    def validate_links(self, links):
        clean_links = []
        clean_url = self.url.split('www.')[1].split('.')[0]
        for l in links:
            if (len(l['href']) < 2) or (l['href'].startswith('tel')) or (l['href'].startswith('mailto')) or (l['href'].startswith('#')) or (l['href'].startswith('javascript')) or (l['href'].startswith('//')):
                continue
            if (l['href'] == '/') or (l['href'] == self.url) or (l['href'] == self.url.split('://')[1]):
                continue
            if (l['href'].startswith('/')):
                clean_links.append(l)
                clean_links[len(clean_links) - 1]['href'] = self.url[:-1] + l['href']
            elif (l['href'].startswith(self.url)) or (l['href'].startswith(self.url.split('://')[1])):
                clean_links.append(l)
                clean_links[len(clean_links) - 1]['href'] = l['href']
        return clean_links            

    def bfs_visit(self):
        if (self.debug):
            out = open('debug_links/' + self.url.split('www.')[1].split('/')[0] + '.txt', 'w')
        # print ("Getting data from (" + self.url + "):")
        for visit_quantity in tqdm(range(self.MAX_VISITS), desc=("Getting data from (" + self.url + ")")):
            html = requests.get(self.url + self.order.pop(0), headers=self.headers)
            if (html.status_code != 200):
                continue
            soup = BeautifulSoup(html.text, 'html.parser')
            # out.write(html.text)
            # out.write('\n\n')
            links = soup.find_all('a', href=True)
            if (self.debug):
                for l in links:
                    out.write(l['href'])
                    out.write('\n')
                out.write('\n')

            links = self.validate_links(links)
            if (self.debug):
                for l in links:
                    out.write(l['href'])
                    out.write('\n')
            # time.sleep(1)
        print ("Done")
        
        if (self.debug):
            out.close()

if (__name__ == "__main__"):
    p = PreProcessing("../../site.txt")
    sites = p.get_sites_info()
    for s in sites:
        c = CrawlerBFS(s, True)
        c.bfs_visit()