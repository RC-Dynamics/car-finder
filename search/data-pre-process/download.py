import requests
import os as sys
import csv
import pandas as pd
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

def download():
    with open("./html/sites_raw2.csv", 'w') as outcsv:
        writer = csv.writer(outcsv)
        words_list = ["link"] + ['html']
        writer.writerow(words_list)
        for file in sys.listdir("."):
            if(file.endswith("2.csv")):
                link = 0
                buff = []
                data = pd.read_csv(file)
                for idx, row in data.iterrows():
                    try:
                        print("Getting: " + row["link"])
                        html = requests.get(row["link"], headers=headers, timeout = 5)
                        if (html.status_code != 200):
                            print("ERROR -----------")
                        else :
                            buff = []
                            buff.append(row["link"])
                            buff.append(html.text)
                            writer.writerow(buff)
                            link += 1
                            time.sleep(1.5)
                    except (requests.exceptions.Timeout): 
                        print("TIMEOUT link: %s"%(row["link"]))
                
    return

if __name__ == "__main__":
    download()  