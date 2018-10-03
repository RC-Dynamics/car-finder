import requests
import os as sys
import pandas as pd
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

def download():
    for file in sys.listdir("./data/links"):
        if(file.endswith(".csv")):
            link = 0
            data = pd.read_csv("data/links/"+file)
            for idx, row in data.iterrows():
                try:
                    print(row["link"])
                    html = requests.get(row["link"], headers=headers, timeout = 5)
                    if (html.status_code != 200):
                        print("ERROR -----------")
                    else :
                        if row["status"] == 1:
                            pos = open("data/html/"+ file[:-4]+ " - " + str(link) + " - pos.html", "w+")
                            pos.write(html.text)
                            page = pos.read()
                            pos.close
                            link += 1
                        elif row["status"] == 0:
                            neg = open("data/html/"+ file[:-4]+ " - " + str(link) + " - neg.html", "w+")
                            neg.write(html.text)
                            neg.close
                            link += 1
                        time.sleep(0.5)
                except (requests.exceptions.Timeout): 
                    print("TIMEOUT link: %s"%(row["link"]))
                
    return

if __name__ == "__main__":
    download()  