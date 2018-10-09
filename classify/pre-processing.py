from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import mutual_info_classif

import os as sys
import csv
from tqdm import tqdm

import numpy as np
import pickle

def removeSpecial(txt):
    symbols = ['\n','/', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '|', '=', ':', '\\', '*', '>', '<']
    for a in symbols:
        txt = txt.replace(a, " ")
    return txt


def makeBoW(name, texts, words):
    with open('./data/dataset/'+name+".csv", 'w') as outcsv:
        writer = csv.writer(outcsv)
        words_list = ["name"] + words + ['status']
        writer.writerow(words_list)
        x , y = 0, 0
        for file in tqdm(texts.keys()):
            if(file.endswith(".txt")):
                y += 1
                row = [str(file[:-8])]
                for w in words:
                    if w in texts[file]:
                        row.append(1)
                    else:
                        row.append(0)
                if file.endswith("pos.txt"):
                    row.append(1)
                elif file.endswith("neg.txt"):
                    row.append(0)
                # print(len(row))
                writer.writerow(row)
                x = len(row)
        print("Saving DB: %s, with Size: (%d, %d)\n"%(name, x, y))



def makeRawCorpus():
    corpus = set()
    files = {}
    corpus_txt = []
    Y  = []

################# Creating all corpus ###################
    for file in tqdm(sys.listdir("./data/txt")):
        if(file.endswith(".txt")):
            f = open("./data/txt/"+file, "r+")
            page = f.read()
            f.close()
            page = removeSpecial(page)
            corpus =  corpus | set(word_tokenize(page))
            files[file] = list(set(word_tokenize(page)))

            corpus_txt.append(page)
            if file.endswith("pos.txt"):
                Y.append(1)
            else:
                Y.append(0)

    with open ("./data/dataset/corpus/corpus.cp", 'wb') as fp:
        pickle.dump(list(corpus), fp)
    
    with open ("./data/dataset/corpus/files.cp", 'wb') as fp:
        pickle.dump(files, fp)
    
    with open ("./data/dataset/corpus/corpus_txt.cp", 'wb') as fp:
        pickle.dump(corpus_txt, fp)

    with open ("./data/dataset/corpus/Y.cp", 'wb') as fp:
        pickle.dump(Y, fp)
    
    return corpus, files, corpus_txt, Y

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
    Y = []
    with open ("./data/dataset/corpus/corpus.cp", 'rb') as fp:
        corpus = pickle.load(fp)
    
    with open ("./data/dataset/corpus/files.cp", 'rb') as fp:
        files = pickle.load(fp)
    
    with open ("./data/dataset/corpus/corpus_txt.cp", 'rb') as fp:
        corpus_txt = pickle.load(fp)

    with open ("./data/dataset/corpus/Y.cp", 'rb') as fp:
        Y = pickle.load(fp)
    
    return corpus, files, corpus_txt, Y

def bowRaw(files, corpus):
    # Creating and saving the dataset raw as csv
    print("Raw: ")
    makeBoW("db1", files, list(corpus))
                
def bowLower(files):
################### FILTERS - LOWER #######################
    corpus_lower = set ()
    for key in files: #LOWER
        for w in range(len(files[key])):
            files[key][w] = (files[key][w]).lower()
        corpus_lower |= set(files[key])
        files[key] = list(set(files[key]))
    corpus_lower = list(corpus_lower)

    print("Lower: ")
    makeBoW("db2", files, corpus_lower)
    return files, corpus_lower

def bowStopwords(files):
#################### FILTERS - STOPWORDS ####################
    stopWords = set(stopwords.words('english'))
    corpus_stop = set()
    for key in files:
        files[key] = list(set(files[key]) - stopWords)
        corpus_stop |= set(files[key])
    corpus_stop = list(corpus_stop)

    print("Lower + noStopWords: ")
    makeBoW("db3", files, corpus_stop)
    return files, corpus_stop

def bowStemming(files):
################### FILTERS - STEMMING #####################
    ps = PorterStemmer()
    corpus_stem = set()
    for key in files:
        for w in range(len(files[key])):
            files[key][w] = ps.stem(files[key][w])
        corpus_stem |= set(files[key])
        files[key] = list(set(files[key]))
    
    corpus_stem = list(corpus_stem)

    print("Lower + noStopWords + Stemming: ")
    makeBoW("db4", files, corpus_stem)
    return files, corpus_stem

def bowVectorizer1(files, corpus_txt):
################### FILTERS  - sklearn - max df = 0.9 ####################

    vectorizer = TfidfVectorizer(max_df = 0.9, max_features = 1000)
    vectorizer.fit_transform(corpus_txt)

    print("Lower + noStopWords + max df x idf + : ")
    makeBoW("db5", files, vectorizer.get_feature_names())
    return vectorizer.get_feature_names()

def bowVectorizer2(files, corpus_txt):
################### FILTERS - max df = 0.8 # min df = 0.2 #############

    vectorizer = TfidfVectorizer(max_df = 0.8, min_df = 0.2, max_features = 1000)
    vectorizer.fit_transform(corpus_txt)

    print("Lower + noStopWords + max & min df x idf : ")
    makeBoW("db6", files, vectorizer.get_feature_names())
    return vectorizer.get_feature_names()

def bowInfogain(files, corpus_txt, Y):
################## FILTERS - Info Gain ################################
    cv = CountVectorizer(max_df=0.9, min_df=0.05, max_features=1000, stop_words='english')
    vector = cv.fit_transform(corpus_txt)
    
    res = dict(zip(cv.get_feature_names(), mutual_info_classif(vector, Y, discrete_features=True)))
    avg = np.average(list(res.values()))
    print("Information Gain ThreshHold: %f"%(avg))

    corpus_info_gain = []
    for key, value in res.items():
        if(value > avg):
            corpus_info_gain.append(key)
    print("Lower + noStopWords + max & min df x idf + InfoGain: ")
    makeBoW("db7", files, corpus_info_gain)
    
    return corpus_info_gain

            
def main():

    # corpus, files, corpus_txt, Y = makeRawCorpus()
    
    corpus, files, corpus_txt, Y  = getRawCorpus()

    bowRaw(files, corpus)

    files_low, corpus_low = bowLower(files)

    files_stop, corpus_stop = bowStopwords(files_low)

    files_stemming, corpus_stemming = bowStemming(files_stop)

    saveCorpus("lowStopStem", corpus_stemming)
######

    corpus_vec1 = bowVectorizer1(files, corpus_txt)

    saveCorpus("vector1", corpus_vec1)

    corpus_vec2 = bowVectorizer2(files, corpus_txt)

    saveCorpus("vector2", corpus_vec2)

    corpus_infogain = bowInfogain(files, corpus_txt, Y)
    
    saveCorpus("infoGain", corpus_infogain)


if __name__ == "__main__":
    main()
