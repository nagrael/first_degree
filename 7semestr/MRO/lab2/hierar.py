import time
from collections import defaultdict, Counter
from functools import partial
from itertools import combinations, product, islice
from scipy.spatial.distance import euclidean, correlation
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.cluster.hierarchy import dendrogram
import community.community_louvain


def main():
    karate()
    dolphins()


def karate():
    karate_kids = nx.karate_club_graph()
    plot_graph(nx.convert_node_labels_to_integers(karate_kids),'karate')


def dolphins():
    G = nx.read_gml('dolphins.gml')
    plot_graph(nx.convert_node_labels_to_integers(G),'dolphins')


def plot_graph(graph,name):
    sparse_adjacency = nx.adjacency_matrix(graph)
    dense_adjacency = sparse_adjacency.todense()
    plot_modularity(graph,name)
    plot_hierarchical(graph, dense_adjacency,name)



def dist_euclidean(u, v, matrix):
    return euclidean(matrix[u], matrix[v])


def dist_correlation(u, v, matrix):
    return np.abs(correlation(matrix[u], matrix[v]))


def dist_shortest(u, v, graph):
    return nx.shortest_path_length(graph, u, v)


def plot_hierarchical(graph, adjacency,name):
    dist_func = {
        'euclidean': partial(dist_euclidean, matrix=adjacency),
        'correlation': partial(dist_correlation, matrix=adjacency),
        'shortest_path': partial(dist_shortest, graph=graph)
    }
    for method in [np.min, np.max, np.mean]:
        for metric in dist_func.keys():
            start_time = time.time()

            linkage = hierarchical_linkage(adjacency, dist_func[metric], method)
            # print(linkage)
            plot_linkage(graph, linkage)

            stop_time = time.time()
            delta_time = stop_time - start_time
            plt.savefig('draw/{}_{}_{}.png'.format(name, method.__name__, metric))
            print('Method: {}, Metric: {}, Time: {}s'.format(method.__name__, metric, delta_time))


def plot_modularity(graph,name):
    figure = plt.figure(figsize=(10, 15))
    start_time = time.time()
    part = community.best_partition(graph)

    values = [part.get(node) for node in graph.nodes()]
    nx.draw_spring(graph, cmap=plt.get_cmap('Set1'), node_color=values, with_labels=True)
    delta_time = time.time() - start_time
    plt.savefig('draw/{}_modulation.png'.format(name))
    print('Modularity example Time: {}d'.format(delta_time))


def plot_linkage(graph, linkage):
    figure = plt.figure(figsize=(10, 15))

    dendrogram_subplot = figure.add_subplot('211')
    dendrogram_spec = dendrogram(linkage, ax=dendrogram_subplot)

    clusters = get_cluster_classes(dendrogram_spec)
    graph_subplot = figure.add_subplot('212')
    graph_subplot.axis('off')

    colors = [clusters[node] for node in graph.nodes()]
    nx.draw_spring(graph, with_labels=True, ax=graph_subplot,
                   node_color=colors, cmap=plt.get_cmap('Set1'))

    figure.tight_layout(pad=0, h_pad=0, w_pad=0)


def get_cluster_classes(den, label='ivl'):
    cluster_idxs = defaultdict(list)
    for c, pi in zip(den['color_list'], den['icoord']):
        for leg in pi[1:3]:
            i = (leg - 5.0) / 10.0
            if abs(i - int(i)) < 1e-5:
                cluster_idxs[c].append(int(i))

    cluster_classes = {}
    for c, l in cluster_idxs.items():
        for o_l in (den[label][i] for i in l):
            cluster_classes[int(o_l)] = c

    return cluster_classes


def hierarchical_linkage(adjacency, metric, method=np.mean):
    # Implementation of scipy.cluster.hierarchy.linkage as described in manual
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
    linkage_array = []
    size = len(adjacency)
    groups = {v: [v] for v in range(size)}

    for groups_number in range(size - 1):
        group_pairs = list(combinations(groups.keys(), 2))
        group_distances = [calc_dist(groups[group1], groups[group2], method, metric)
                           for group1, group2 in group_pairs]
        # print(group_distances)
        min_distance_index = np.argmin(group_distances)
        min_distance = group_distances[min_distance_index]
        group1, group2 = group_pairs[min_distance_index]
        new_group_members = groups.pop(group1) + groups.pop(group2)
        groups[groups_number + size] = new_group_members

        linkage_entry = [group1, group2, float(min_distance), len(new_group_members)]
        linkage_array.append(linkage_entry)

    return np.array(linkage_array)


def calc_dist(group1, group2, method, metric):
    pairwise_distances = np.array([metric(u, v) for u in group1 for v in group2])
    return method(pairwise_distances)


if __name__ == '__main__':
    main()
