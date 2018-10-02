import pandas as pd
import requests
import os as sys
from bs4 import BeautifulSoup
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

def rawText(html):
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(["style", "scritp"]):
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # print (text)
    return text



def download():
    for file in sys.listdir("."):
        if(file.endswith(".csv")):
            link = 0
            data = pd.read_csv(file)
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


def extractText():
    for file in sys.listdir("./data/html"):
        if(file.endswith(".html")):
            f = open("./data/html/"+file, "r+")
            page = f.read()
            f.close()
            pos = open("data/txt/"+file[:-5]+".txt", "w+")
            pos.write(rawText(page))
            pos.close         
    return


if __name__ == "__main__":
    # download()  
    extractText()