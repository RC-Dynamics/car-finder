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
    extractText()