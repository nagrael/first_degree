import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G, edge_labels):
    pos=nx.circular_layout(G)


    nx.draw_networkx_nodes(G,pos, node_size=400, alpha=0.7)
    nx.draw_networkx_edges(G,pos,width=2.5,alpha=0.5)
    nodes_labels = dict([(x, x) for x in G.nodes()])
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
    nx.draw_networkx_labels(G,pos, labels=nodes_labels, font_size=16)
    plt.axis('off')
    plt.savefig("foto")
    plt.show()