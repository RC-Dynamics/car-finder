import nltk
nltk.download('punkt')

import pandas as pd
import os
from nltk.tokenize import word_tokenize
import pickle
import pprint
from sklearn import svm


class URL_Classify:
    path = ''
    debug = False

    def __init__(self, links_path, debug=False):
        self.path = links_path
        self.debug = debug
        if self.debug:
            self.pp = pprint.PrettyPrinter(indent=4)

    def remove_special(self, txt):
        symbols = ['\n','/', '.com', '.uk', '&', '+', '%', 'www.', '_', '.ca', '.co', 'jhtml', 'html', 'https', 'http', ',', '.', '"', '-', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '|', '=', ':', '\\', '*', '>', '<']
        for a in symbols:
            txt = txt.replace(a, " ")
        return txt

    def make_raw_corpus(self):
        corpus = set()
        files = {}
        corpus_txt = []
        Y  = []
        link = 0
        for file in os.listdir('./' + self.path):
            if(file.endswith(".csv")):
                data = pd.read_csv(self.path + '/' + file)
                for _, row in data.iterrows():
                    words = self.remove_special(row['link'])
                    corpus =  corpus | set(word_tokenize(words))
                    files[link] = list(set(word_tokenize(words)))

                    Y.append(int(row['status']))
                    link += 1
        if self.debug:
            self.pp.pprint (files)
            self.pp.pprint (Y)
            self.pp.pprint (corpus)
        if self.debug:
            print(len(corpus))
            print(len(files))
            print(len(Y))
        return corpus, files, Y

    def make_bow(self, texts, words, Y):
        bow = []
        # bow.append(['name'] + words + ['Y'])
        for idx, obj in texts.items():
            row = []
            # row = [idx]
            for w in words:
                if w in obj:
                    row.append(1)
                else:
                    row.append(0)
            # row.append(Y[idx])
            bow.append(row)
        if self.debug:
            print(len(bow))
        return bow

    def train (self):
        corpus, files, Y = self.make_raw_corpus()
        X = self.make_bow(files, list(corpus), Y)

        svr_model = svm.SVR(gamma='auto')
        svr_model.fit(X, Y)
        # print (svr_model.predict([X[0]]))

        pickle.dump(svr_model, open('svr_model.sav', 'wb'))
        pickle.dump(list(corpus), open('corpus.sav', 'wb'))

if (__name__ == "__main__"):
    classify = URL_Classify('data/links', debug=False)
    classify.train()