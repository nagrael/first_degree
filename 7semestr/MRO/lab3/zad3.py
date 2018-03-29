import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import make_circles
from sklearn.svm import SVC

names = ["Linear SVM", "RBF SVM", "Poly SVM"]

classifiers = [
    SVC(kernel='linear'),
    SVC(kernel='rbf', gamma=0.7),
    SVC(kernel='poly', degree=3)]


def main():
    plt.figure(figsize=(18, 5))
    x, y = make_circles(n_samples=400, factor=.3, noise=.05)
    ax = plt.subplot(1, len(classifiers) + 1, 1)
    ax.set_title("Original space")
    reds = y == 0
    blues = y == 1
    ax.scatter(x[reds, 0], x[reds, 1], c="red",
               s=20, edgecolor='k')
    ax.scatter(x[blues, 0], x[blues, 1], c="blue",
               s=20, edgecolor='k')
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")

    x_min, x_max = x[:, 0].min() - 0.5, x[:, 0].max() + 0.5
    y_min, y_max = x[:, 1].min() - 0.5, x[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, .02),
                         np.arange(y_min, y_max, .02))
    i = 2
    for name, clf in zip(names, classifiers):
        ax = plt.subplot(1, len(classifiers) + 1, i)
        clf.fit(x, y)

        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

        Z = Z.reshape(xx.shape)
        ax.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=.8)

        ax.scatter(x[:, 0], x[:, 1], c=y, cmap=plt.cm.Paired,
                   edgecolors='k')

        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xticks(())
        ax.set_yticks(())

        ax.set_title(name)
        ax.set_xlabel("$x_1$")
        ax.set_ylabel("$x_2$")
        i += 1
    plt.show()


if __name__ == "__main__":
    main()
