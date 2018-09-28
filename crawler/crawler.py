import requests
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import sys
sys.path.append('pre_processing')

from pre_processing import PreProcessing

class Crawler:
    url = ''
    order = []
    disallow = []
    visited = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    MAX_VISITS = 1
    debug = False

    def __init__(self, site, dbg=False):
        self.url = site['site']
        self.order = []
        self.order.append('/')
        self.disallow = site['disallow']
        self.visited = []
        self.debug = dbg

    def is_not_allowed(self, path):
        if (path in self.disallow):
            return True
        for l in filter(lambda x: x[-1] == '/', self.disallow):
            if (path.startswith(l)):
                return True
        for l in filter(lambda x: '*' in x, self.disallow):
            link_parts = l.split('*')
            if len(link_parts[0]) > 1 and len(link_parts[1]) > 1:
                if path.startswith(link_parts[0]) and link_parts[1] in path:
                    return True
            else:
                if len(link_parts[0]) > 1:
                    if path.startswith(link_parts[0]):
                        return True
                if len(link_parts[1]) > 1:
                    if link_parts[1] in path:
                        return True
        return False   

    def validate_links(self, links):
        clean_links = []
        for l in links:
            if (len(l['href'].strip()) < 2):
                continue
            if (len(l['href']) < 2) or (l['href'].startswith('tel')) or (l['href'].startswith('mailto')) or (l['href'].startswith('#')) or (l['href'].startswith('javascript')) or (l['href'].startswith('//')) or (l['href'].startswith('\t')):
                continue
            if (l['href'] == '/') or (l['href'] == self.url) or (l['href'] == self.url.split('://')[1]):
                continue
            if (l['href'].startswith('/')):
                clean_links.append(l)
                clean_links[len(clean_links) - 1]['href'] = l['href']
            elif (l['href'].startswith(self.url)) or (l['href'].startswith(self.url.split('://')[1])):
                clean_links.append(l)
                clean_links[len(clean_links) - 1]['href'] = l['href'].split(self.url[:-1])[1]
        return clean_links  

    def evaluate_links(self, links, method):
        if (method == 'heuristic'):
            pass
        elif (method == 'ml'):
            pass
        else:
            for l in links:
                if (l['href'] in self.visited) or (l['href'] in self.order) or (self.is_not_allowed(l['href'])):
                    continue
                self.order.append(l['href'])

    def get_links(self, visiting_now):
        html = requests.get(self.url[:-1] + visiting_now, headers=self.headers)
        if (html.status_code != 200):
            return -1
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup.find_all('a', href=True)

    def visit(self, method='bfs'):
        if (self.debug):
            out = open('debug_links/' + self.url.split('www.')[1].split('/')[0] + '.txt', 'w')
        for visit_quantity in tqdm(range(self.MAX_VISITS), desc=("Getting data from (" + self.url + ")")):
            visiting_now = self.order.pop(0)
            if (visiting_now in self.visited) or (self.is_not_allowed(visiting_now)):
                visit_quantity -= 1
                continue
            self.visited.append(visiting_now)

            links = self.get_links(visiting_now)
            
            links = self.validate_links(links)

            self.evaluate_links(links, method)
            
            if (links == -1):
                visit_quantity -= 1
                continue
            if (self.debug):
                for l in links:
                    out.write(l['href'])
                    out.write('\n')

            # time.sleep(1)
        print ("Done")
        
        if (self.debug):
            out.close()

if (__name__ == "__main__"):
    p = PreProcessing("../site.txt")
    sites = p.get_sites_info()
    for s in sites:
        c = Crawler(s, True)
        c.visit()