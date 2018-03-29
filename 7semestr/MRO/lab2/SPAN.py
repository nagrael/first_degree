import time
from collections import defaultdict, Counter

from itertools import combinations, tee

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.cluster.hierarchy import dendrogram
import community.community_louvain


def main():
    print('Load started')
    # G = nx.read_edgelist('com-dblp.ungraph.txt')
    G = nx.read_edgelist('email-Eu-core.txt')
    print('Load completed')
    print('Ground true: 13,477')
    print("Communities detected using modulation")
    part = community.best_partition(G)
    print(len(set(part.values())))

    plot_girvan_newman(nx.convert_node_labels_to_integers(G))


def plot_girvan_newman(graph):
    start_time = time.time()

    linkage = compute_girvan_newman_linkage(graph.copy())
    plt.figure()
    dendrogram_spec = dendrogram(linkage)

    print('Detected {} clusters'.format(len(dendrogram_spec['color_list'])))

    delta_time = time.time() - start_time

    plt.savefig('girvan_newman.png')
    plt.show()
    print('Girvan-Newman, Time: {}s'.format(delta_time))


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."

    for elem in range(len(iterable) - 1):
        yield tuple(((iterable[elem], iterable[elem + 1])))


# def pairwise(iterable):
#     "s -> (s0,s1), (s1,s2), (s2, s3), ..."
#     a, b = tee(iterable)
#     next(b, None)
#     return zip(a, b)

def compute_girvan_newman_linkage(graph):
    history = []
    edges = nx.number_of_edges(graph)
    print('Starting removing edges.')
    k = 0

    for _ in range(edges):
        print('Iteration {}'.format(k))
        start = time.time()
        edges_counter = Counter()
        # for node1, node2 in combinations(nodes, 2):
        try:
            path = nx.all_pairs_shortest_path(graph)
            print('Paths calculated in {}s '.format(time.time() - start))
            # print(path)
            for i in path.keys():
                for j in path[i].keys():
                    try:
                        edges = pairwise(path[i][j])

                        edges_counter.update(edges)
                    except KeyError:
                        pass

        except nx.NetworkXNoPath:
            pass
        u, v = edges_counter.most_common(1)[0][0]
        graph.remove_edge(u, v)
        history.append((u, v))
        k += 1
        print('Time {}s'.format(time.time() - start))
    history.reverse()
    print('Starting building clusters.')
    groups = {node: [node] for node in graph.nodes()}
    nodes_number = len(groups)
    linkage_array = []
    link_number = 0

    for node1, node2 in history:
        group1 = None
        group2 = None

        for group, nodes in groups.items():
            if node1 in nodes:
                group1 = group

            if node2 in nodes:
                group2 = group

        if group1 != group2:
            new_group_members = groups.pop(group1) + groups.pop(group2)
            groups[nodes_number + link_number] = new_group_members
            link_number += 1

            linkage_entry = [group1, group2, float(link_number), len(new_group_members)]
            linkage_array.append(linkage_entry)

    return np.array(linkage_array)


if __name__ == "__main__":
    main()
