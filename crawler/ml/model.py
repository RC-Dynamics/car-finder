import nltk
nltk.download('punkt')

import pickle
import pprint
from nltk.tokenize import word_tokenize
from sklearn import svm

def remove_special(txt):
    symbols = ['\n','/', '.com', '.uk', '&', '+', '%', 'www.', '_', '.ca', '.co', 'jhtml', 'html', 'https', 'http', ',', '.', '"', '-', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '|', '=', ':', '\\', '*', '>', '<']
    for a in symbols:
        txt = txt.replace(a, " ")
    return txt

def svr_link_ranking(url):
    svr_mode = pickle.load(open('ml/svr_model.sav', 'rb'))
    corpus = pickle.load(open('ml/corpus.sav', 'rb'))
    url = remove_special(url)
    url = list(set(word_tokenize(url)))
    row = []
    for word in corpus:
        if word in url:
            row.append(1)
        else:
            row.append(0)
    return svr_mode.predict([row])[0]