import requests
import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import sys
sys.path.append('pre_processing')
sys.path.append('heuristic')

from pre_processing import PreProcessing
from anchor import get_anchor_weights

class Crawler:
    url = ''
    order = []
    disallow = []
    visited = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    MAX_VISITS = 1000
    debug = False
    error = None
    out = None
    link_words = get_anchor_weights()

    def __init__(self, site, dbg=False):
        self.url = site['site']
        self.order = []
        self.order.append({'link': '/', 'score': 1})
        self.disallow = site['disallow']
        self.visited = []
        self.debug = dbg
        if (self.debug):
            if 'www.' in self.url:
                self.out = open('debug_links/' + self.url.split('www.')[1].split('/')[0] + '.txt', 'w')
            else:
                self.out = open('debug_links/' + self.url.split('https://')[1].split('/')[0] + '.txt', 'w')

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
            if (l['href'].startswith('//')):
                l['href'] = l['href'].strip('/')
            if (len(l['href'].strip()) < 2):
                continue
            if (len(l['href']) < 2) or (l['href'].startswith('tel')) or (l['href'].startswith('mailto')) or (l['href'].startswith('#')) or (l['href'].startswith('javascript')) or (l['href'].startswith('\t')):
                continue
            if (l['href'] == '/') or (l['href'] == self.url) or (l['href'] == self.url.split('://')[1]) or ('AuthRedirect' in l['href']):
                continue
            if (l['href'].startswith('/')):
                clean_links.append(l)
                clean_links[len(clean_links) - 1]['href'] = l['href']
            elif (l['href'].startswith(self.url.split('://')[1])):
                clean_links.append(l)
                clean_links[len(clean_links) - 1]['href'] = l['href'].split(self.url.split('://')[1][:-1])[1].strip('"')
            elif (l['href'].startswith(self.url)):
                clean_links.append(l)
                clean_links[len(clean_links) - 1]['href'] = l['href'].split(self.url[:-1])[1].strip('"')
        return clean_links  

    def evaluate_links(self, links, method):
        if (method == 'heuristic'):
            for l in links:
                if (l['href'] in self.visited) or (l['href'] in [o['link'] for o in self.order]) or (self.is_not_allowed(l['href'])):
                    continue
                new_item = {'link': l['href'], 'score': 1}
                for anchor in self.link_words:
                    qtd = len(list(filter(lambda x: x in new_item['link'], anchor['words'])))
                    if qtd:
                        new_item['score'] *= qtd * anchor['weight']

                self.order.append(new_item)

            self.order.sort(key=lambda x: x['score'], reverse=True)

            pass
        elif (method == 'ml'):
            pass
        else:
            for l in links:
                if (l['href'] in self.visited) or (l['href'] in [o['link'] for o in self.order]) or (self.is_not_allowed(l['href'])):
                    continue
                self.order.append({'link': l['href'], 'score': 1})

    def print_error(self, error_type, error_msg):
        self.error = open('errors.txt', 'a')
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
        self.error.write(error_type + ' (' + st + '): ' + error_msg)
        self.error.write('\n')
        self.error.close()

    def print_debug(self, links):
        if (self.debug):
            self.out.write('ALL LINKS:')
            self.out.write('\n')
            for l in links:
                self.out.write(l['href'])
                self.out.write('\n')
            self.out.write('\n\n')
        
        if (self.debug):
            self.out.write('VISIT ORDER:')
            self.out.write('\n')
            for l in self.order:
                self.out.write(str('%.2f'%(l['score'])) + '\t\t - ' + l['link'])
                self.out.write('\n')
            self.out.write('\n-----------------------------------------------------------------------------\n\n')

    def get_links(self, visiting_now):
        try:
            html = requests.get(self.url[:-1] + visiting_now, headers=self.headers, timeout=5)
        except requests.exceptions.Timeout:
            self.print_error('TIMEOUT', self.url[:-1] + visiting_now)
            return -1
        if (html.status_code != 200):
            return -1
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup.find_all('a', href=True)

    def save_visited_csv(self, method):
        df = pd.DataFrame(list(map(lambda x: self.url[:-1] + x, self.visited)), columns=["visited_links"])
        if 'www.' in self.url:
            df.to_csv('results/' + method + '/' + self.url.split('www.')[1][:-1] + '.csv', header=True, index=False, encoding='utf-8')
        else:
            df.to_csv('results/' + method + '/' + self.url.split('https://')[1][:-1] + '.csv', header=True, index=False, encoding='utf-8')

    def visit(self, method='bfs', save_results=False):
        for visit_quantity in tqdm(range(self.MAX_VISITS), desc=("Getting data from (" + self.url + ")")):
            if not self.order:
                self.print_error('NOT ENOUGH LINK: ', self.url)
                break
            visiting_now = self.order.pop(0)['link']
            if (visiting_now in self.visited) or (self.is_not_allowed(visiting_now)):
                visit_quantity -= 1
                continue
            self.visited.append(visiting_now)

            if (self.debug):
                self.out.write('VISITING NOW: ' + visiting_now)
                self.out.write('\n')
            
            links = self.get_links(visiting_now)
            if (links == -1):
                visit_quantity -= 1
                continue

            self.print_debug(links)            
                
            links = self.validate_links(links)

            self.evaluate_links(links, method)
            
            time.sleep(0.5)
        if save_results:
            self.save_visited_csv(method)
        print ("Done")
        
        if (self.debug):
            self.out.close()

if (__name__ == "__main__"):
    p = PreProcessing("../site.txt")
    sites = p.get_sites_info()
    for s in sites:
        c = Crawler(s, dbg=False)
        c.visit(method='heuristic', save_results=True)