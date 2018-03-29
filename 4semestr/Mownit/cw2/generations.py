import random
def generate(n,m):
    nodes = [x for x in range(1, n+1)]
    with open("name.txt",'w')as file:
        for s in range(m):
            x = random.sample(nodes,2)
            f = random.uniform(0.0,100.0)
            string = "("+str(x[0])+","+str(x[1])+","+str(f)+")\n"
            file.write(string)
        x = random.sample(nodes,2)
        f = random.uniform(0.0,100.0)
        string = "Voltage: ("+str(x[0])+","+str(x[1])+","+str(f)+")"
        file.write(string)