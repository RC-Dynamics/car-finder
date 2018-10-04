import pandas as pd
from numpy import ravel
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate
from output import *

def main():
    dfs = ['../data/db1.csv', '../data/db2.csv', '../data/db3.csv', '../data/db4.csv', '../data/db5.csv', '../data/db6.csv']

    param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000] }
    clft = GridSearchCV(linear_model.LogisticRegression(penalty='l2'), param_grid)
    
    f = createFile("Logistic_Regression")
    
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

        clf = linear_model.LogisticRegression(C=(clft.best_params_)['C'])
        folders = 10

        scores = cross_validate(clf, X, y, cv=folders, scoring=('accuracy', 'precision', 'recall'), return_train_score=True, n_jobs=2)

        printResults(scores)
        saveResults(f, scores, path)

        title = "Logistic_Regression_" + path[-7:-4]
        plot_learning_curve(clf, title, X, y, cv=folders, n_jobs=2)


        
if __name__ == "__main__":
    main()
