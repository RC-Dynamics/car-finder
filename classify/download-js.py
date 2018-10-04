import requests
import os as sys
import pandas as pd
import time
from selenium import webdriver

def download():
    for file in sys.listdir("./data/links"):
        if(file.endswith(".csv")):
            link = 0
            data = pd.read_csv("data/links/"+file)
            for idx, row in data.iterrows():
                try:
                    driver = webdriver.PhantomJS()
                    print("Getting: " + row["link"])
                    driver.get(row["link"])
                    html = driver.page_source
                    driver.close()
                    # html = requests.get(row["link"], headers=headers, timeout = 5)
                    if row["status"] == 1:
                        pos = open("data/html/"+ file[:-4]+ " - " + str(link) + " - pos.html", "w+")
                        pos.write(html)
                        time.sleep(0.05)
                        pos.close()
                        link += 1
                    elif row["status"] == 0:
                        neg = open("data/html/"+ file[:-4]+ " - " + str(link) + " - neg.html", "w+")
                        neg.write(html)
                        time.sleep(0.05)
                        neg.close()
                        link += 1
                    time.sleep(1)
                except (requests.exceptions.Timeout): 
                    print("TIMEOUT link: %s"%(row["link"]))
                
    return

if __name__ == "__main__":
    download()  