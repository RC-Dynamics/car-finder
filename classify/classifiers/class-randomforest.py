import pandas as pd
from numpy import ravel
from numpy.core.umath_tests import inner1d
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from output import *

def main():
    dfs = ['../data/db1.csv', '../data/db2.csv', '../data/db3.csv', '../data/db4.csv', '../data/db5.csv', '../data/db6.csv', '../data/db7.csv']
    
    f = createFile("Random_Forest")
    

    for path in dfs:
        print("\n"+path)
        df = pd.read_csv(path)
        X = df.ix[:,1:df.shape[1]-1]
        y = df.ix[:,df.shape[1]-1:df.shape[1]]

        X = X.values
        y = y.values
        
        y = ravel(y)
        
        clf = RandomForestClassifier(n_estimators=500, random_state=0)
        folders = 10

        scores = cross_validate(clf, X, y, cv=folders, scoring=('accuracy', 'precision', 'recall'), return_train_score=True, n_jobs=3)

        printResults(scores)
        saveResults(f, scores, path)

        title = "Random_Forest_" + path[-7:-4]
        plot_learning_curve(clf, title, X, y, cv=folders, n_jobs=4)

        
if __name__ == "__main__":
    main()
