import pandas as pd
import requests
import os as sys
from bs4 import BeautifulSoup
import time
import csv

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

def extractText():
    with open("./html/sites_txt.csv", 'w+') as outcsv:
        writer = csv.writer(outcsv)
        words_list = ["link"] + ['html']
        writer.writerow(words_list)
        for file in sys.listdir("./html"):
                if(file.endswith("raw.csv")):
                    print(file)
                    data = pd.read_csv("./html/"+file)
                    for idx, row in data.iterrows():
                        print("Cleaning: " + row["link"])
                        buff = []
                        buff.append(row["link"])
                        buff.append(rawText(row["html"]))
                        writer.writerow(buff)        
    return


if __name__ == "__main__":
    extractText()