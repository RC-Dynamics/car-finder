import pandas as pd
from numpy import ravel
from numpy.core.umath_tests import inner1d
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate
from output import *


# {'max_depth': 7, 'max_features': 'log2', 'n_estimators': 200}

def main():
    dfs = ['../data/dataset/db1.csv', '../data/dataset/db2.csv', '../data/dataset/db3.csv', '../data/dataset/db4.csv', '../data/dataset/db5.csv', '../data/dataset/db6.csv', '../data/dataset/db7.csv']
    
    f = createFile("Random_Forest")
    

    param_grid = { 
        'n_estimators': [200, 500],
        'max_features': ['auto', 'sqrt', 'log2'],
        'max_depth' : [5,6,7,8],
    }
    rfc = RandomForestClassifier(random_state=0)
    CV_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv = 3)
    findingParam = True
    paramns = {}

    for path in dfs:
        print("\n"+path)
        df = pd.read_csv(path)
        X = df.ix[:,1:df.shape[1]-1]
        y = df.ix[:,df.shape[1]-1:df.shape[1]]

        X = X.values
        y = y.values
        
        y = ravel(y)

        if findingParam:
            findingParam = False
            print("Finding Parameters...")
            CV_rfc.fit(X, y,)
            paramns = CV_rfc.best_params_
            print(paramns)

        
        clf = RandomForestClassifier(n_estimators=paramns["n_estimators"], max_features=paramns["max_features"], max_depth=paramns["max_depth"] , random_state=0)
        folders = 10

        scores = cross_validate(clf, X, y, cv=folders, scoring=('accuracy', 'precision', 'recall'), return_train_score=True, n_jobs=2)

        printResults(scores)
        saveResults(f, scores, path)

        title = "Random_Forest_" + path[-7:-4]
        plot_learning_curve(clf, title, X, y, cv=folders, n_jobs=2)

        
if __name__ == "__main__":
    main()
