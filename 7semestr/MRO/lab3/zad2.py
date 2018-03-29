import numpy as np
from matplotlib import pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def main():
    iris = datasets.load_iris()
    x_train, x_test, y_train, y_test = \
        train_test_split(iris.data, iris.target, test_size=1 / 3)

    names = ["Linear SVM", "RBF SVM", "Poly SVM", "Nearest Neighbors"]

    classifiers = [
        SVC(kernel='linear'),
        SVC(kernel='rbf', gamma=0.7),
        SVC(kernel='poly', degree=3),
        KNeighborsClassifier(1)]
    i =1

    for name, classifier in zip(names, classifiers):
        classifier.fit(x_train, y_train)
        y_result = classifier.predict(x_test)
        print(name)
        print(classification_report(y_test, y_result))

    names = ["Linear SVM", "RBF SVM", "Poly SVM"]

    classifiers = [
        SVC(kernel='linear'),
        SVC(kernel='rbf', gamma=0.7),
        SVC(kernel='poly', degree=3)]
    pca = PCA(2)
    x = pca.fit_transform(iris.data)
    y = iris.target
    figure = plt.figure(figsize=(15, 7))
    x_min, x_max = x[:, 0].min() - 0.5, x[:, 0].max() + 0.5
    y_min, y_max = x[:, 1].min() - 0.5, x[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, .02),
                         np.arange(y_min, y_max, .02))
    for name, clf in zip(names, classifiers):
        ax = plt.subplot(1, len(classifiers), i)
        clf.fit(x, y)

        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        ax.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=.8)

        # Plot also the training points
        ax.scatter(x[:, 0], x[:, 1], c=y, cmap=plt.cm.Paired,
                   edgecolors='k')
        # and testing points
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xticks(())
        ax.set_yticks(())

        ax.set_title(name)

        i += 1
    plt.show()



if __name__ == "__main__":
    main()
