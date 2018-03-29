from copy import copy, deepcopy
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from numpy import array

import networkx as nx
from numpy import linalg, matrix, random
import matplotlib.pyplot as plt
import  numpy as NP
from scipy.sparse.linalg import eigs, norm
from scipy.sparse import  csr_matrix


#float('inf')
from scipy.stats import histogram


def dominate_value_jump(mx, pos_vec):

    x1 = csr_matrix(random.rand(mx.shape[0], 1))
    x1 = x1/norm(x1,ord=float('inf'))
    x2 = x1
    x1 = mx.dot(x1)
    d = norm(x2,ord=float('inf')) - norm(x1,ord=float('inf'))
    x1 = x1 + csr_matrix(d*pos_vec)
    x1 = x1/norm(x1,ord=float('inf'))
    while abs(norm(x1-x2)) > 0.01:

        x2 = x1
        x1 = mx.dot(x1)
        d = norm(x2,ord=float('inf')) - norm(x1,ord=float('inf'))
        x1 = x1 + csr_matrix(d*pos_vec)
        x1 = x1/norm(x1,ord=float('inf'))

    hist, bins = NP.histogram((x1/norm(x1,ord=float('inf'))).todense(),len(x))

    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()
def dominate_value(mx):

    x1 = csr_matrix(random.rand(mx.shape[0], 1))
    x2 = x1
    print(x1.todense())
    x1 =  mx* x1

    print(norm(x1,ord=float('inf')))
    x1 = x1/norm(x1,ord=float('inf'))

    while abs(norm(x1-x2)) > 0.0000001:
        print(x1.todense())
        print('\n')
        x2 = x1
        x1 = mx.dot(x1)
        x1 = x1/norm(x1,ord=float('inf'))

    print((x1/norm(x1)).todense())

DG=nx.DiGraph()
DG.add_nodes_from([i for i in range(7115)])
with open ("Wiki-Vote.txt", 'r') as f:
    for lines in f:
        x1 = lines.split()[0]
        x2 = lines.split()[1]
        DG.add_edge(x1, x2)
        print("ADD")



#DG = nx.gnc_graph(1000)
print('c')
a = nx.adjacency_matrix(DG,nodelist=nx.nodes(DG),weight=None).todense().tolist()
y = [random.uniform(0,0.1) for x in nx.nodes(DG)]
print('a')
nodes_labels = dict([(x, x) for x in DG.nodes()])
pos=nx.circular_layout(DG)
#nx.draw_networkx_labels(DG, pos, labels=nodes_labels, font_size=16)
#nx.draw(DG,pos)
for x in a:
    s = sum(x)
    if s != 0:
        for y in range(len(x)):
            x[y] = (x[y])/(s)

#print(eigs(csr_matrix(a)))
y = [random.uniform(0,0.1) for x in nx.nodes(DG)]
#plt.show()
dominate_value_jump(csr_matrix(a), matrix(y).getT())
#dominate_value(csr_matrix(b))

