import requests

class PreProcessing:
    robots = "robots.txt"
    sites = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    debug = False
    
    def __init__(self, file_path, debug=False):
        self.debug = debug
        file_site = open(file_path, "r")
        self.sites = list({"site": s[:-1]} for s in file_site.readlines())
        file_site.close()
        self.get_robots()

    def get_robots(self):
        if(self.debug):
            out = open("test.txt", "w")
        for s in self.sites:
            if(self.debug):
                print (s['site'])
            r = requests.get(s['site'] + self.robots, headers=self.headers)
            s['robots'] = r.text
            s['status_code'] = r.status_code
        for s in self.sites:
            if (s['status_code'] != 200):
                self.sites.remove(s)
        if(self.debug):
            for s in self.sites:        
                out.write(s['site'] + " - " + str(s['status_code']) + "\n\n")
                out.write(s['robots'])
        if(self.debug):
            out.close()
        self.get_disallow()

    def get_disallow(self):
        for s in self.sites:
            result_data_set = {"Disallowed":[], "Allowed":[]}
            for line in s['robots'].split("\n"):
                if line.startswith('Allow'):    # this is for allowed url
                    if (len(line.split(': ')) > 1):
                        result_data_set["Allowed"].append(line.split(': ')[1].split(' ')[0].strip('#').strip(' ').strip('\t').strip('\n').strip('\r'))    # to neglect the comments or other junk info
                elif line.startswith('Disallow'):    # this is for disallowed url
                    if (len(line.split(': ')) > 1):
                        result_data_set["Disallowed"].append(line.split(': ')[1].split(' ')[0].strip('#').strip(' ').strip('\t').strip('\n').strip('\r'))    # to neglect the comments or other junk info
            s['disallow'] = result_data_set["Disallowed"]
            del s['robots']


    def print_info(self):
        for s in self.sites:
            print('site:\t\t{0} \nstatus_code:\t{1} \ndisallow:\t{2}\n\n'.format(
                s['site'],
                s['status_code'],
                s['disallow'])
            ) 

    def get_sites_info(self):
        return self.sites

if (__name__ == "__main__"):
    p = PreProcessing("../site.txt")
    p.print_info()