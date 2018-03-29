from input_hand import get_data
from draw import draw_graph
from calculate import calculate_all
from generations import generate
import networkx as nx


def main():
    #generate(1000, 7000)
    edges, nodes, v = get_data('name.txt')
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    label = calculate_all(G,v)
    draw_graph(G, label)


if __name__ == '__main__':
    main()

