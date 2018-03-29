from matplotlib import pyplot as plt
import numpy as np
from sklearn import svm


def main():
    x = np.random.randint(0, 15, size=(2, 30))
    y = np.random.randint(15, 30, size=(2, 30))
    X = np.concatenate((x.T, y.T),axis=0)

    Y = [0] * 30 + [1] * 30
    plt.scatter(x[0], x[1], c='r')
    plt.scatter(y[0], y[1],  c='g')
    plt.show()
    clf = svm.SVC(kernel='linear')
    clf.fit(X, Y)

    # get the separating hyperplane
    w = clf.coef_[0]
    a = -w[0] / w[1]
    xx = np.linspace(0, 30)
    yy = a * xx - (clf.intercept_[0]) / w[1]


    margin = 1 / np.sqrt(np.sum(clf.coef_ ** 2))
    yy_down = yy + a * margin
    yy_up = yy - a * margin


    plt.plot(xx, yy, 'k-')
    plt.plot(xx, yy_down, 'k--')
    plt.plot(xx, yy_up, 'k--')
    plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=80,
                facecolors='none', zorder=10, edgecolors='k')
    plt.scatter(X[:, 0], X[:, 1], c=Y, zorder=10, cmap=plt.cm.Paired,
                edgecolors='k')

    plt.show()
if __name__ == "__main__":
    main()