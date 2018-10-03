import pandas as pd
from numpy import ravel
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate


def main():
    dfs = ['../data/db1.csv', '../data/db2.csv', '../data/db3.csv', '../data/db4.csv', '../data/db5.csv', '../data/db6.csv']

    param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000] }
    clft = GridSearchCV(linear_model.LogisticRegression(penalty='l2'), param_grid)
    
    f = open("logisticRegression.txt", "w+")
    f.write("Logistic Regression\n")
    
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

        scores = cross_validate(clf, X, y, cv=folders, scoring=('accuracy', 'precision', 'recall'), return_train_score=True)

        print("Train Accuracy: %0.2f (+/- %0.2f)" % (scores["train_accuracy"].mean(), scores["train_accuracy"].std() * 2))
        print("Test Accuracy: %0.2f (+/- %0.2f)" % (scores["test_accuracy"].mean(), scores["test_accuracy"].std() * 2))
        print("Precision: %0.2f (+/- %0.2f)" % (scores["test_precision"].mean(), scores["test_precision"].std() * 2))
        print("Recall: %0.2f (+/- %0.2f)" % (scores["test_recall"].mean(), scores["test_recall"].std() * 2))
        print("Fit Time: %0.2f (+/- %0.2f)" % (scores["fit_time"].mean(), scores["fit_time"].std() * 2))
        print('\n')
        f.write(path)
        f.write("\nTrain Accuracy: %0.2f (+/- %0.2f)\n" % (scores["train_accuracy"].mean(), scores["train_accuracy"].std() * 2))
        f.write("Teste Accuracy: %0.2f (+/- %0.2f)\n" % (scores["test_accuracy"].mean(), scores["test_accuracy"].std() * 2))
        f.write("Precision: %0.2f (+/- %0.2f)\n" % (scores["test_precision"].mean(), scores["test_precision"].std() * 2))
        f.write("Recall: %0.2f (+/- %0.2f)\n" % (scores["test_recall"].mean(), scores["test_recall"].std() * 2))
        f.write("Fit Time: %0.2f (+/- %0.2f)\n" % (scores["fit_time"].mean(), scores["fit_time"].std() * 2))
        f.write('\n\n')

        
if __name__ == "__main__":
    main()
