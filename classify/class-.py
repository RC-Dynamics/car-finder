import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import time


def main():
    dfs = ['./data/db1.csv', './data/db2.csv', './data/db3.csv', './data/db4.csv', './data/db5.csv']

    for path in dfs:
        print('\n\n' + path)
        df = pd.read_csv(path)
        X = df.ix[:,1:df.shape[1]-1]
        y = df.ix[:,df.shape[1]-1:df.shape[1]]

        X = X.values
        y = y.values
        
        y = np.ravel(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
        
        clf = GaussianNB()
        folders = 10
        
        scores = cross_val_score(clf, X, y, cv=folders)
        #print(scores)
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        
        scores = cross_val_score(clf, X, y, cv=folders, scoring='precision')
        #print(scores)
        print("Precision: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        
        scores = cross_val_score(clf, X, y, cv=folders, scoring='recall')
        #print(scores)
        print("Recall: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

        start_time = time.time()
        clf.fit(X_train, y_train)
        end_time = time.time()
        print("fit time %g seconds" % (end_time - start_time))



if __name__ == "__main__":
    main()
