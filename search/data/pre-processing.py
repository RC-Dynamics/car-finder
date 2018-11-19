from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel

import os as sys
import csv
import json
from tqdm import tqdm
import pandas as pd
import numpy as np
import pickle

def removeSpecial(txt):
    symbols = ['\n','/', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '|', '=', ':', '\\', '*', '>', '<', '2c', '22', '3a', 'div', 'u002f', 'u002f', 'u003c', 'u003e']
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
    
    with open ("./corpus/files_corpus.cp", 'rb') as fp:
        files = pickle.load(fp)
    
    with open ("./corpus/corpus_raw.cp", 'rb') as fp:
        corpus_txt = pickle.load(fp)
    
    return corpus, files, corpus_txt
                
def bowInfogain(files, corpus_txt):
################## FILTERS - Info Gain ################################
    cv = CountVectorizer(max_df=0.9, min_df=0.05, stop_words='english')
    
    # print(cv.inverse_transform(vector))
    # features = cv.get_feature_names()
    # print (corpus_txt[0])
    # print (vector)
    # print (features)
    return cv.fit_transform(corpus_txt), cv.get_feature_names()

            
def main():
    querry = ["chevrolet", "car"]
    # corpus, files, corpus_txt = makeRawCorpus()
    
    corpus, files, corpus_txt = getRawCorpus()

    vector, features = bowInfogain(files, corpus_txt)
    
    keys = list(files.keys())
    j = 0
    dictionary = {}
    for fet in features:
        dictionary[fet] = []
        # print(fet)
        i = 0
        for vec in vector.toarray():
            if vec[j] != 0:
                temp = {}
                temp["doc"] = int(i)
                temp["freq"] = int(vec[j])
                dictionary[fet].append(temp)
            i += 1
        j += 1
    with open('index.json', 'w') as fp:
        json.dump(dictionary, fp)
    

    



    # cosine_similarities = linear_kernel(vector[0:1], vector).flatten()
    # print (cosine_similarities)
    # print (vector.shape)
    # document = 0
    # for i in vector:
    #     print(i)
    #     document += 1
    #     break
        



    


if __name__ == "__main__":
    main()
