from nltk import ngrams, FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

import os as sys
import csv
from tqdm import tqdm

def removeSpecial(txt):
    symbols = ['\n','/', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '|', '=', ':', '\\', '*', '>', '<']
    for a in symbols:
        txt = txt.replace(a, " ")
    return txt


def makeBoW(name, texts, words):
    with open('./data/'+name+".csv", 'w') as outcsv:
        writer = csv.writer(outcsv)
        words_list = ["name"] + words + ['status']
        writer.writerow(words_list)
        x , y = 0, 0
        for file in tqdm(sys.listdir("./data/txt")):
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
                else:
                    row.append(0)
                # print(len(row))
                writer.writerow(row)
                x = len(row)
        print("Saving DB: %s, with Size: (%d, %d)\n"%(name, x, y))



def main():
    corpus = set()
    corpus_txt = []
    files = {}

################# Collecting all corpus ###################
    for file in tqdm(sys.listdir("./data/txt")):
        if(file.endswith(".txt")):
            f = open("./data/txt/"+file, "r+")
            page = f.read()
            f.close()
            page = removeSpecial(page)
            corpus =  corpus | set(word_tokenize(page))
            corpus_txt.append(page)
            files[file] = list(set(word_tokenize(page)))
    
    # Saving the corpus 
    # f = open('./data/raw-data.txt', 'w')
    # f.write(str(list(corpus))[1:-1])
    # f.close()

    # Creating and saving the dataset raw as csv
    makeBoW("db1", files, list(corpus))
                

################### FILTERS - LOWER #######################
    corpus_lower = set ()
    for key in files: #LOWER
        for w in range(len(files[key])):
            files[key][w] = (files[key][w]).lower()
        corpus_lower |= set(files[key])
        files[key] = list(set(files[key]))
    corpus_lower = list(corpus_lower)

    print("Lower: ", end = "")
    makeBoW("db2", files, corpus_lower)
    
#################### FILTERS - STOPWORDS ####################

    stopWords = set(stopwords.words('english'))
    for key in files:
        files[key] = list(set(files[key]) - stopWords)
    corpus_stop = list(set(corpus_lower) - stopWords)

    print("Lower + noStopWords: ", end = "")
    makeBoW("db3", files, corpus_stop)
    


################### FILTERS - STEMMING #####################

    ps = PorterStemmer()
    corpus_stem = set()
    for key in files:
        for w in range(len(files[key])):
            files[key][w] = ps.stem(files[key][w])
        corpus_stem |= set(files[key])
        files[key] = list(set(files[key]))
    
    corpus_stem = list(corpus_stem)

    print("Lower + noStopWords + Stemming: ", end = "")
    makeBoW("db4", files, corpus_stem)

################### FILTERS  - sklearn - max df = 0.9 ####################

    vectorizer = TfidfVectorizer(max_df = 0.9, max_features = 1000)
    vectorizer.fit_transform(corpus_txt)

    print("Lower + noStopWords + Stemming + max df x idf + : ", end = "")
    makeBoW("db5", files, vectorizer.get_feature_names())

################### FILTERS - max df = 0.8 # min df = 0.2 #############

    vectorizer = TfidfVectorizer(max_df = 0.8, min_df = 0.2, max_features = 1000)
    vectorizer.fit_transform(corpus_txt)

    print("Lower + noStopWords + Stemming + max & min df x idf + : ", end = "")
    makeBoW("db6", files, vectorizer.get_feature_names())




if __name__ == "__main__":
    main()
