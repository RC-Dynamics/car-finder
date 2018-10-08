import pandas as pd
import numpy as np
from numpy import ravel
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_validate
from output import *


def main():
    dfs = ['../data/dataset/db1.csv', '../data/dataset/db2.csv', '../data/dataset/db3.csv', '../data/dataset/db4.csv', '../data/dataset/db5.csv', '../data/dataset/db6.csv', '../data/dataset/db7.csv']
    
    f = createFile("Naive_Bayes")

    for path in dfs:
        print('\n' + path)
        df = pd.read_csv(path)
        X = df.ix[:,1:df.shape[1]-1]
        y = df.ix[:,df.shape[1]-1:df.shape[1]]

        X = X.values
        y = y.values
        
        y = ravel(y)
        
        clf = GaussianNB()
        folders = 10
        
        scores = cross_validate(clf, X, y, cv=folders, scoring=('accuracy', 'precision', 'recall'), return_train_score=True, n_jobs=3)
        
        printResults(scores)
        saveResults(f, scores, path)

        title = "Naive_Bayes_" + path[-7:-4]
        plot_learning_curve(clf, title, X, y, cv=folders, n_jobs=4)



if __name__ == "__main__":
    main()
