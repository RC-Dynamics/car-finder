from nltk.tokenize import word_tokenize
from numpy.core.umath_tests import inner1d
import pandas as pd
import pickle
from tqdm import tqdm
import os as sys
import csv

def removeSpecial(txt):
    symbols = ['\n','/', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '|', '=', ':', '\\', '*', '>', '<']
    for a in symbols:
        txt = txt.replace(a, " ")
    return txt

def makeRawCorpus(name):
    files = {}
################# Creating all corpus ###################
    for file in tqdm(sys.listdir("./"+name)):
        if(file.endswith(".csv")):
            df = pd.read_csv("./"+name+"/"+file)        
            X = df.values
            for link in tqdm(X):
                page = removeSpecial(link[1])
                files[link[0]] = set(word_tokenize(page))
    return files


def makeBoW(name, texts, words):
    with open('./'+name+"/" + name + "_bow.csv", 'w') as outcsv:
        writer = csv.writer(outcsv)
        words_list = ["name"] + words
        writer.writerow(words_list)
        x , y = 0, 0
        for file in tqdm(texts.keys()):
            y += 1
            row = [str(file[:])]
            for w in words:
                if w in texts[file]:
                    row.append(1)
                else:
                    row.append(0)
            writer.writerow(row)
            x = len(row)
        print("Saving DB: %s, with Size: (%d, %d)\n"%(name, x, y))


def main():
    name = "bfs" # or heuristic or bfs or ml
    files = makeRawCorpus(name)
    # Saving files dict filtered
    with open ("./"+name+"/"+name+"_raw.cp", 'wb') as fp:
        pickle.dump(files, fp)
    
    # Loading files dict
    files = {}
    with open ("./"+name+"/"+name+"_raw.cp", 'rb') as fp:
        files = pickle.load(fp)

    # Loading Corpus
    corpus = []
    with open ("../data/dataset/corpus/corpus.cp", 'rb') as fp:
        corpus = pickle.load(fp)

    # Building Bag of Words
    makeBoW(name, files, corpus)
    # Size: (27410, 7279)

    # Loading Bag of Words
    df = pd.read_csv("./"+name+"/"+name+"_bow.csv") 
    X = df.values
    label = df.ix[:,0]
    X = df.ix[:,1:df.shape[1]]
    
    # Loading Model
    clf = pickle.load(open("../classifiers/model/ensemble.ml", 'rb'))
    result = clf.predict(X)

    # Saving Results
    with open('./'+name+'_result.csv', 'w') as outcsv:
        writer = csv.writer(outcsv)
        words_list = ["name", "result"]
        writer.writerow(words_list)
        y = 0
        for i in tqdm(range(len(result))):
            row = []
            row.append(label[i])
            row.append(result[i])
            writer.writerow(row)
            y += 1
        print ("Predict: %d sites"%(y))



if __name__ == "__main__":
    main()