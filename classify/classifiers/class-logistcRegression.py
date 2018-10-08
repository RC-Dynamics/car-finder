import pandas as pd
from numpy import ravel
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate
from output import *

# {'C': 0.1}

def main():
    dfs = ['../data/dataset/db1.csv', '../data/dataset/db2.csv', '../data/dataset/db3.csv', '../data/dataset/db4.csv', '../data/dataset/db5.csv', '../data/dataset/db6.csv', '../data/dataset/db7.csv']

    param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000] }
    clft = GridSearchCV(linear_model.LogisticRegression(penalty='l2'), param_grid)
    
    f = createFile("Logistic_Regression")
    findingParam = True

    for path in dfs:
        print('\n'+path)
        df = pd.read_csv(path)
        X = df.ix[:,1:df.shape[1]-1]
        y = df.ix[:,df.shape[1]-1:df.shape[1]]

        X = X.values
        y = y.values
        
        y = ravel(y)

        if findingParam:
            print("Find parameters...")
            clft.fit(X,y)
            paramns = clft.best_params_
            print(paramns)
            findingParam = False

        clf = linear_model.LogisticRegression(C=(clft.best_params_)['C'])
        folders = 10

        scores = cross_validate(clf, X, y, cv=folders, scoring=('accuracy', 'precision', 'recall'), return_train_score=True, n_jobs=2)

        printResults(scores)
        saveResults(f, scores, path)

        title = "Logistic_Regression_" + path[-7:-4]
        plot_learning_curve(clf, title, X, y, cv=folders, n_jobs=2)


        
if __name__ == "__main__":
    main()
