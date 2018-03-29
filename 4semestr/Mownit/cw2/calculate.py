import networkx as nx
from scipy import linalg


def calculate_all(G, v):
    result = []
    edge_weight = nx.get_edge_attributes(G,'weight')
    edge_non = nx.edges(G)
    cycle = nx.cycle_basis(G)
    A = nx.adj_matrix(G, weight=None).todense().tolist()
    final_result =[]

    for lists in cycle:
        # From graphs cycles gets second Kirchhoff law
        tmp = [0]*(len(edge_weight)+2)
        result.append(0)
        for calc_result in range(len(lists)-1):
            y = (lists[calc_result],lists[calc_result+1])
            if A[y[1]-1][y[0]-1] and A[y[0]-1][y[1]-1]:
                A[y[1]-1][y[0]-1] = 0
                if y[1] > y[0]:
                    tmp[edge_non.index(y)] = - edge_weight[y]
                else:
                    y = tuple(reversed(y))
                    tmp[edge_non.index(y)] = -edge_weight[y]

            else:
                if A[y[0]-1][y[1]-1]:
                    if y[1] > y[0]:
                        tmp[edge_non.index(y)] = - edge_weight[y]
                    else:
                        y = tuple(reversed(y))
                        tmp[edge_non.index(y)] = -edge_weight[y]
                else:
                    if y[1] > y[0]:
                        tmp[edge_non.index(y)] = + edge_weight[y]
                    else:
                        y = tuple(reversed(y))
                        tmp[edge_non.index(y)] = + edge_weight[y]
        final_result.append(tmp)
    for edge in G.nodes():
        tmp = [0]*(len(edge_weight)+2)
        result.append(0)
        for y in G.edges(edge):
            if A[y[1]-1][y[0]-1] and A[y[0]-1][y[1]-1]:
                A[y[1]-1][y[0]-1] = 0
                if y[1] > y[0]:
                    tmp[edge_non.index(y)] = - 1
                else:
                    y = tuple(reversed(y))
                    tmp[edge_non.index(y)] = -1

            else:
                if A[y[0]-1][y[1]-1]:
                    if y[1] > y[0]:
                        tmp[edge_non.index(y)] = - 1
                    else:
                        y = tuple(reversed(y))
                        tmp[edge_non.index(y)] = -1
                else:
                    if y[1] > y[0]:
                        tmp[edge_non.index(y)] = 1
                    else:
                        y = tuple(reversed(y))
                        tmp[edge_non.index(y)] = 1
        if edge == v[0]:
            tmp[len(tmp)-2] = 1
        if edge == v[1]:
            tmp[len(tmp)-1] = -1

        final_result.append(tmp)
        leng = nx.shortest_path_length(G ,v[0], v[1])
    for short_path in nx.all_simple_paths(G,v[0],v[1],cutoff=(leng+1)):
        tmp = [0]*(len(edge_weight)+2)
        result.append(v[2])
        for calc_result in range(len(short_path)-1):
            y = (short_path[calc_result],short_path[calc_result+1])
            if A[y[1]-1][y[0]-1] and A[y[0]-1][y[1]-1]:
                A[y[1]-1][y[0]-1] = 0
                if y[1] > y[0]:
                    tmp[edge_non.index(y)] = - edge_weight[y]
                else:
                    y = tuple(reversed(y))
                    tmp[edge_non.index(y)] = -edge_weight[y]

            else:
                if A[y[0]-1][y[1]-1]:
                    if y[1] > y[0]:
                        tmp[edge_non.index(y)] = - edge_weight[y]
                    else:
                        y = tuple(reversed(y))
                        tmp[edge_non.index(y)] = -edge_weight[y]
                else:
                    if y[1] > y[0]:
                        tmp[edge_non.index(y)] = + edge_weight[y]
                    else:
                        y = tuple(reversed(y))
                        tmp[edge_non.index(y)] = + edge_weight[y]
        final_result.append(tmp)
    try:
        calc_result = linalg.solve(final_result,result).tolist()
        del calc_result[len(calc_result)-1]
        del calc_result[len(calc_result)-1]
    except:
        calc_result = linalg.lstsq(final_result,result)[0].tolist()
        del calc_result[len(calc_result)-1]
        del calc_result[len(calc_result)-1]
    for m in range(len(calc_result)):
        edge_weight[edge_non[m]] = round(abs(calc_result[m]),10)
    return edge_weight

