from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

import os as sys
import csv
from tqdm import tqdm
import pandas as pd
import numpy as np
import pickle

def removeSpecial(txt):
    symbols = ['\n','/', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '|', '=', ':', '\\', '*', '>', '<']
    for a in symbols:
        txt = txt.replace(a, " ")
    return txt

def makeRawCorpus():
    corpus = set()
    files = {}
    corpus_txt = []
    Y  = []

################# Creating all corpus ###################
    for file in (sys.listdir("./html")):
        if(file.endswith("txt.csv")):
            data = pd.read_csv("./html/"+file)
            for idx, row in tqdm(data.iterrows()):
                page = row["html"]
                page = removeSpecial(page)
                corpus =  corpus | set(word_tokenize(page))
                files[row["link"]] = list(set(word_tokenize(page)))
                corpus_txt.append(page)

    with open ("./corpus/corpus.cp", 'wb') as fp:
        pickle.dump(list(corpus), fp)
    
    with open ("./corpus/files_corpus.cp", 'wb') as fp:
        pickle.dump(files, fp)
    
    with open ("./corpus/corpus_raw.cp", 'wb') as fp:
        pickle.dump(corpus_txt, fp)
    
    return corpus, files, corpus_txt

def loadCorpus(name):
    corpus = []
    with open ("./data/dataset/corpus/"+ name +".cp", 'rb') as fp:
        corpus = pickle.load(fp)
    return corpus

def saveCorpus(name, corpus):
    with open ("./data/dataset/corpus/"+ name +".cp", 'wb') as fp:
        pickle.dump(corpus, fp)
    
def getRawCorpus():
    corpus = []
    files = {}
    corpus_txt = []

    with open ("./corpus/corpus.cp", 'rb') as fp:
        corpus = pickle.load(fp)
    
    with open ("./corpus/files.cp", 'rb') as fp:
        files = pickle.load(fp)
    
    with open ("./corpus/corpus_txt.cp", 'rb') as fp:
        corpus_txt = pickle.load(fp)
    
    return corpus, files, corpus_txt
                
def bowInfogain(files, corpus_txt):
################## FILTERS - Info Gain ################################
    cv = CountVectorizer(max_df=0.9, min_df=0.05, max_features=1000, stop_words='english')
    vector = cv.fit_transform(corpus_txt)
    # print (vector)

    return []

            
def main():

    corpus, files, corpus_txt = makeRawCorpus()
    
    # corpus, files, corpus_txt, Y  = getRawCorpus()

    corpus_infogain = bowInfogain(files, corpus_txt)
    


if __name__ == "__main__":
    main()
