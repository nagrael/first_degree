
def get_data(file_name):
    edges = []
    nodes = set()
    with open(file_name, 'r') as file:
        for line in file:
            if line[0] is not 'V':
                node = [int(line.strip('( )\n').split(sep=',')[i]) for i in range(2)]
                nodes.update(set(node))
                node.append({'weight':float(line.strip('( )\n').split(sep=',')[2])})
                edges.append(node)
            else:
                v = [float(line.strip('Voltage: ()').split(sep=',')[i]) for i in range(3)]
                v[0] = int(v[0])
                v[1] = int(v[1])

    return edges,(list(nodes)),v
