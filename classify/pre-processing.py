from nltk import ngrams, FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stemmer import PorterStemmer as ps
 


# import nltk
# lemma = nltk..wordnet.WordNetLemmatizer()
# lemma.lemmatize('article')
# 'article'
# lemma..lemmatize('leaves')
# 'leaf'


def main():
    comments = ""
    comments += "Diego pegue seu beco que ja ta mas na hora. A pepa ja ta lhe aguardando"
    comments += " "
    comments += "Não entendo por que a percentagem do Diego estão caindo! E Jéssica esta na frente da Gleice."
    comments += " "
    comments += "O povo ensisti querer tirar a gleice. Mais não entende que ela que ser a dona do meio milhão. Chupa canbada que querem tirar a Gleice"
    comments += " "
    comments += "Pela quantidade de votos sai o Diego eu queria que saísse a pela saco da Jessica."

    comments = comments.lower()

    ps.stem("token")

    stopWords = set(stopwords.words('english'))
    stopWords.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
    stem
    words = word_tokenize(comments)
    wordsFiltered = []
    for w in words:
        if w not in stopWords:
            wordsFiltered.append(w)


    wordsCount = FreqDist(ngrams(wordsFiltered, 1))
    d = dict(wordsCount)
    wordsDict = dict((key[0], value) for (key, value) in d.items())

    sorted_x = sorted(wordsDict.items(), key=operator.itemgetter(1), reverse = True)

    print(sorted_x[0:5])


if __name__ == "__main__":
    main()
