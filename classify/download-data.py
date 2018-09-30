import pandas as pd
import requests
import os as sys
from bs4 import BeautifulSoup

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
    link_p = 0
    link_n= 0
    for file in sys.listdir("."):
        if(file.endswith(".csv")):
            data = pd.read_csv(file)
            for idx, row in data.iterrows():
                html = requests.get(row["link"], headers=headers)
                if (html.status_code != 200):
                    print("ERROR -----------")
                else :
                    if row["status"] == 1:
                        pos = open("data/pos/"+file[:-4]+"-"+str(link_p)+".html", "w+")
                        pos.write(html.text)
                        page = pos.read()
                        pos.close
                        link_p += 1
                    elif row["status"] == 0:
                        neg = open("data/neg/"+file[:-4]+"-"+str(link_n)+".html", "w+")
                        neg.write(html.text)
                        neg.close
                        link_n += 1
    return


def extractText():
    link_p = 0
    link_n= 0
    for file in sys.listdir("./data/pos"):
        if(file.endswith(".html")):
            f = open("./data/pos/"+file, "r+")
            page = f.read()
            f.close()
            pos = open("data/pos/"+file[:-5]+".txt", "w+")
            pos.write(rawText(page))
            pos.close
            link_p += 1
    for file in sys.listdir("./data/neg"):
        if(file.endswith(".html")):
            f = open("./data/neg/"+file, "r+")
            page = f.read()
            f.close()
            neg = open("data/neg/"+file[:-5]+".txt", "w+")
            neg.write(rawText(page))
            neg.close
            link_n += 1
                    
    return


if __name__ == "__main__":
    # download()
    extractText()