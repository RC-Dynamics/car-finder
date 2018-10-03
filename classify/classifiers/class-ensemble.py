import pandas as pd
from numpy import ravel
from numpy.core.umath_tests import inner1d

from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn import linear_model
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_validate


def main():
    dfs = ['../data/db1.csv', '../data/db2.csv', '../data/db3.csv', '../data/db4.csv', '../data/db5.csv', '../data/db6.csv']
    
    f = open("ensemble.txt", "w+")
    f.write("Ensemble\n")
    
    for path in dfs:
        print('\n'+path)
        df = pd.read_csv(path)
        X = df.ix[:,1:df.shape[1]-1]
        y = df.ix[:,df.shape[1]-1:df.shape[1]]

        X = X.values
        y = y.values
        
        y = ravel(y)

        clf1 = RandomForestClassifier(n_estimators=500, random_state=0)
        clf2 = linear_model.LogisticRegression(C=0.01)
        clf3 = svm.SVC()
        clf4 = GaussianNB()
        clf5 = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 5), random_state=1)
        
        eclf = VotingClassifier(estimators=[('rf', clf1), ('lr', clf2), ('svm', clf3), ('nb', clf4), ('mlp', clf5)], voting='hard')
        folders = 10

        scores = cross_validate(eclf, X, y, cv=folders, scoring=('accuracy', 'precision', 'recall'), return_train_score=True)

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