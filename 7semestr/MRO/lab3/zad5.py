
from collections import defaultdict
import numpy as np
from matplotlib import pyplot as plt
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_lfw_people
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def main():
    lfw_people = fetch_lfw_people(min_faces_per_person=70)
    _, h, w = lfw_people.images.shape
    x = lfw_people.data
    y = lfw_people.target
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    pca = PCA(150, svd_solver='randomized', whiten=True).fit(x_train)
    #eigenfaces = pca.components_.reshape((150, h, w))
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1),
                             algorithm="SAMME",
                             n_estimators=200)
    #eigenface_titles = ["eigenface %d" % i for i in range(eigenfaces.shape[0])]
    #plot_gallery(eigenfaces, eigenface_titles, h, w)

    plt.show()

    x_test_pca = pca.transform(x_test)
    x_train_pca = pca.transform(x_train)
    k=1
    classifier = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1),
                             algorithm="SAMME",
                             n_estimators=k)
    classifier.fit(x_train_pca, y_train)
    y_pred = classifier.predict(x_test_pca)
    print(classification_report(y_test, y_pred, target_names=lfw_people.target_names))
    for i, name in enumerate(lfw_people.target_names):
        accuracy = accuracy_score(y_test == i, y_pred == i)
        print (name + " accuracy: " + str(accuracy))
    person_accuracies = defaultdict(list)
    sizes = list(range(1,50,5))
    for k in sizes:
        classifier = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1),
                             algorithm="SAMME",
                             n_estimators=k)
        classifier.fit(x_train_pca, y_train)
        y_pred = classifier.predict(x_test_pca)
        for i, name in enumerate(lfw_people.target_names):
            accuracy = accuracy_score(y_test == i, y_pred == i)
            person_accuracies[name].append(accuracy)
    for name, accuracies in person_accuracies.items():
        plt.plot(sizes, accuracies, '-', label=name)
    plt.legend(ncol=2, loc=3)
    plt.ylabel('accuracy')
    plt.xlabel('k')
    plt.ylim(0, 1)
    plt.show()


def plot_gallery(images, titles, h, w, n_row=2, n_col=5):
    """Helper function to plot a gallery of portraits"""
    plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(n_row * n_col):
        plt.subplot(n_row, n_col, i + 1)
        plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
        plt.title(titles[i], size=12)
        plt.xticks(())
        plt.yticks(())


if __name__ == '__main__':
    main()