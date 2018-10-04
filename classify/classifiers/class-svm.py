import pandas as pd
from numpy import ravel
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate
from output import *

def main():
    dfs = ['../data/db1.csv', '../data/db2.csv', '../data/db3.csv', '../data/db4.csv', '../data/db5.csv', '../data/db6.csv', '../data/db7.csv']

    grid_param = {'C': [ 0.01, 0.1, 1, 10, 100, 1000], 'kernel': [ 'rbf', 'linear', 'poly', 'sigmoid']}
    clft = GridSearchCV(svm.SVC(), grid_param)

    f = createFile("SVM")
    
    first = True
    for path in dfs:
        print('\n'+path)
        df = pd.read_csv(path)
        X = df.ix[:,1:df.shape[1]-1]
        y = df.ix[:,df.shape[1]-1:df.shape[1]]

        X = X.values
        y = y.values
        
        y = ravel(y)
        if first:
            print("Find parameters...")
            clft.fit(X,y)
            paramns = clft.best_params_
            print(paramns)
            first = False
        
        clf = svm.SVC(C = paramns['C'], kernel = paramns['kernel'])
        folders = 10

        scores = cross_validate(clf, X, y, cv=folders, scoring=('accuracy', 'precision', 'recall'), return_train_score=True, n_jobs=2)

        printResults(scores)
        saveResults(f, scores, path)

        title = "SVM_" + path[-7:-4]
        plot_learning_curve(clf, title, X, y, cv=folders, n_jobs=2)

        
if __name__ == "__main__":
    main()
