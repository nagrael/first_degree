import os
import time
from functools import partial
import matplotlib.pyplot as plt
import numpy as np
import shutil
from scipy import io as io
from scipy.spatial.distance import euclidean, mahalanobis
from random import choice
from  sklearn.neighbors import KDTree
from sklearn.neighbors import DistanceMetric
import pandas as pd


def main():
    faces, images = load_faces()

    images_to_vector = {tuple(vector): image for vector, image in zip(faces, images)}
    mahalanobis_distance = partial(mahalanobis, VI=np.linalg.inv(np.cov(faces.T)))
    mahalanobis_distance.__name__ = 'mahalanobis'

    random_init = random_centroids
    random_init.__name__ = 'random_centroids'
    k_plus_plus_generation = k_plus_plus
    k_plus_plus_generation.__name__ = 'k_plus_plus_generation'
    for metric in [euclidean, mahalanobis_distance]:
        tree_search = partial(kd_tree_search, tree=kd_tree(faces, metric.__name__))
        tree_search.__name__ = 'kdtree'
        n_search = partial(normal_search, metric=metric)
        n_search.__name__ = 'normal_search'
        for k in [2, 5, 8, 10]:
            for init in [random_init, k_plus_plus_generation]:
                if metric.__name__ == 'mahalanobis':
                    args = [k, metric, 100, 10, init, n_search]
                    save_kmeans(faces, images_to_vector, args)
                else:
                    for search_t in [n_search, tree_search]:
                        args = [k, metric, 100, 10, init, search_t]
                        save_kmeans(faces, images_to_vector, args)


def kd_tree(vectors, metric):
    if metric == 'euclidean':
        t = DistanceMetric.get_metric('euclidean')
    else:
        print('Mahalanobis cannot be used with kd-tree')
        return None
    # print(KDTree(vectors).valid_metrics)
    kdtree = KDTree(vectors, metric=t)
    return kdtree


def save_kmeans(faces, images_to_vector, args):
    directory = 'tests/k{p[0]}/{p[1].__name__}_it{p[2]}_r{p[3]}_{p[4].__name__}_{p[5].__name__}'.format(p=args)
    print(directory)
    try:
        os.makedirs(directory)
    except OSError:
        print('Warning: removing existing  directory')
        shutil.rmtree(directory)
        os.makedirs(directory)

    start_time = time.time()
    clusters = kmeans(faces, *args)
    delta_time = time.time() - start_time
    print("Metric: {}, k: {}, search method: {}, time: {} ".format(args[1].__name__, args[0], args[5].__name__,
                                                                   delta_time))

    for cluster, vectors in enumerate(clusters):
        figure = plt.figure()
        # print(len(vectors))
        side = np.ceil(np.sqrt(len(vectors))).astype(int)

        for i, vector in enumerate(vectors):
            image = images_to_vector[tuple(vector)]
            similar_subplot = figure.add_subplot(side, side, i + 1)
            similar_subplot.imshow(image, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
            similar_subplot.axis('off')

        figure.tight_layout(pad=0, h_pad=0, w_pad=0)
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        save_path = os.path.join(directory, '{}.png'.format(cluster))
        figure.savefig(save_path)
        plt.close(figure)


def dist_from_centers(vectors, mu, metric):
    return np.array([min([metric(x, c) for c in mu]) for x in vectors])


def choose_next_center(differance_list):
    probs = differance_list / differance_list.sum()
    cumprobs = probs.cumsum()
    r = np.random.random()
    ind = np.where(cumprobs >= r)[0][0]
    return ind


def k_plus_plus(vectors, k, metric):
    mu = [np.array(choice(vectors))]
    while len(mu) < k:
        mu.append(vectors[choose_next_center(dist_from_centers(vectors, mu, metric))])
    return np.array(mu)


def random_centroids(vectors, k, metric):
    vector_min = vectors.min(axis=0)
    vector_max = vectors.max(axis=0)
    vector_range = vector_max - vector_min
    return vector_min + np.random.random(size=(k, vectors.shape[1])) * vector_range


def kd_tree_search(vectors, centroids, k, tree):
    distances, vector = tree.query(centroids, k=vectors.shape[0], return_distance=True)
    wq = list(zip(distances.tolist(), vector.tolist()))
    sorted_dist = ([sorted(list(zip(b, a)), key=lambda c: c[0]) for a, b in wq])
    dist_final = [[distance[1] for distance in centroid] for centroid in sorted_dist]
    dista_to_cent = np.argmin(dist_final, axis=0)
    c_distances = [[] for _ in range(k)]
    c_vectors = [[] for _ in range(k)]
    for i in range(len(dista_to_cent)):
        c_distances[dista_to_cent[i]].append(dist_final[dista_to_cent[i]][i])
        c_vectors[dista_to_cent[i]].append(vectors[i])
    return sum(np.sum(c_distances[centroid]) for centroid in range(k)), c_vectors


def normal_search(vectors, centroids, k, metric=euclidean):
    c_distances = [[] for _ in range(k)]
    c_vectors = [[] for _ in range(k)]
    for vector in vectors:
        distances = [metric(vector, c) for c in centroids]

        centroid_index = np.argmin(distances)
        c_vectors[centroid_index].append(vector)
        c_distances[centroid_index].append(distances[centroid_index])

    return sum(np.sum(c_distances[centroid]) for centroid in range(k)), c_vectors


def kmeans(vectors, k, metric=euclidean, iterations=100, restarts=1, init=k_plus_plus,
           ksearch=normal_search):
    vector_min = vectors.min(axis=0)
    vector_max = vectors.max(axis=0)
    vector_range = vector_max - vector_min

    best_score = np.Inf
    best_result = None
    # print(vector_min)
    for restart in range(restarts):
        # In case of exception

        try:
            centroids = init(vectors, k, metric)
            for i in range(iterations):

                score, c_vectors = ksearch(vectors, centroids, k)
                if score < best_score:
                    best_score = score
                    best_result = [c_vectors[centroid] for centroid in range(k)]

                centroids = np.array([np.mean(c_vectors[centroid], axis=0) for centroid in range(k)])
                empty_centroids = pd.isnull(centroids)

                if empty_centroids.any():
                    # print(centroids)
                    random_size = (sum(empty_centroids), vectors.shape[1])
                    # print(empty_centroids, sum(empty_centroids))
                    new_centroids = vector_min + np.random.random(size=random_size) * vector_range
                    centroids[empty_centroids] = new_centroids

        except ValueError:
            print('Error')
            continue

    print(best_score)
    return best_result


def load_faces():
    data = io.loadmat('facesYale.mat')
    images = np.dstack((data['facesTrain'], data['facesTest']))
    images = images.swapaxes(0, 2)
    images = images.swapaxes(1, 2)
    x = np.vstack((data['featuresTrain'], data['featuresTest']))
    return x, images


if __name__ == '__main__':
    main()
