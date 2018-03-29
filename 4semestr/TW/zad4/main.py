import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

x = [[], [], [], []]
with open("a.txt") as f:
    for line in f:
        x[0].append(int(line.split()[0]))
        x[1].append(int(line.split()[1]))
        x[2].append(int(line.split()[2]))
        x[3].append(int(line.split()[3]))
print(len(x[0]))
print(len(x[1]))
print(len(x[2]))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(x[0],x[1],x[2],cmap=cm.jet)
fig = plt.figure()
bx = fig.add_subplot(111, projection='3d')
bx.plot_trisurf(x[0],x[1],x[3],cmap=cm.jet)
plt.show()