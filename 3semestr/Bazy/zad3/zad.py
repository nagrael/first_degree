import matplotlib.pyplot as plt
import numpy as np

n = 500
x = [0.76]

abc = []
r = [ab*10/n for ab in range(1,int(4*n/10))]
print(r)
for rs in r:
    for a in range(0,n):
        xs = rs*x[len(x)-1]*(1-x[len(x)-1])
        print(x[-1:])
        x.append(xs)
    del x[0]
    del x[0]
    xy = np.array(x)
    abc.append(xy)
    x = [0.76]
abc = np.array(abc)
plt.plot(r, abc)
plt.show()