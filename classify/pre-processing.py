from nltk import ngrams, FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import os as sys
import csv
from tqdm import tqdm

def removeSpecial(txt):
    symbols = ['/', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '|', '=', ':', '\\', '*', '>', '<']
    for a in symbols:
        txt = txt.replace(a, " ")
    return txt

def saveDB(name, texts, words):
    with open('./data/'+name+".csv", 'w') as outcsv:
        writer = csv.writer(outcsv)
        words_list = ["name"] + words + ['status']
        writer.writerow(words_list)
        x , y = 0, 0
        for file in sys.listdir("./data/txt"):
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
        print("Size: (%d, %d)"%(x, y))



def main():
    corpus = set()
    corpus_txt = []
    texts = {}

################# Collecting all corpus ###################
    for file in tqdm(sys.listdir("./data/txt")):
        if(file.endswith(".txt")):
            f = open("./data/txt/"+file, "r+")
            page = f.read()
            f.close()
            page = removeSpecial(page)
            corpus =  corpus | set(word_tokenize(page))
            corpus_txt.append(page)
            texts[file] = word_tokenize(page)
    
    # Saving the corpus 
    f = open('./data/raw-data.txt', 'w')
    f.write(str(list(corpus))[1:-1])
    f.close()

    # Creating and saving the dataset raw as csv
    saveDB("db1", texts, list(corpus))
                

################### FILTERS - LOWER #######################

    for key in texts: #LOWER
        for w in range(len(texts[key])):
            texts[key][w] = (texts[key][w]).lower()
        texts[key] = list(set(texts[key]))
    
    corpus_lower = []
    for w in corpus:
        corpus_lower.append(w.lower())
    corpus_lower = list(set(corpus_lower))


    print("Lower: ", end = "")
    saveDB("db2", texts, corpus_lower)
    
#################### FILTERS - STOPWORDS ####################

    stopWords = set(stopwords.words('english'))
    for key in texts:
        texts[key] = list(set(texts[key]) - stopWords)

    corpus_stop = list(set(corpus_lower) - stopWords)

    print("Lower + noStopWords: ", end = "")
    saveDB("db3", texts, corpus_stop)
    


################### FILTERS - STEMMING #####################

    ps = PorterStemmer()
    for key in texts:
        for w in range(len(texts[key])):
            texts[key][w] = ps.stem(texts[key][w])
        texts[key] = list(set(texts[key]))

    corpus_stem = []
    for w in corpus_stop:
        corpus_stem.append(ps.stem(w))
    corpus_stem = list(set(corpus_stem))

    print("Lower + noStopWords + Stemming: ", end = "")
    saveDB("db4", texts, corpus_stem)

################### FILTERS  - df #####################

    vectorizer = TfidfVectorizer(max_df = 0.9, max_features = 1000)
    vectorizer.fit_transform(corpus_txt)

    saveDB("db5", texts, vectorizer.get_feature_names())




    
    
    
    
    
    


    
    
    


    


if __name__ == "__main__":
    main()
