import random as r
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def generate(t, a):
    return np.array([np.cos(t)*np.sin(a),np.sin(a)*np.sin(t),np.cos(t)])
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x=np.cos(u)*np.sin(v)
y=np.sin(u)*np.sin(v)
z=np.cos(v)

ax.plot_wireframe(x, y, z, color="g")

plt.show()
R1 = np.matrix([[10*r.random() for i in range(3)] for j in range(3)])
R2 = np.matrix([[10*r.random() for i in range(3)] for j in range(3)])
R3 = np.matrix([[10*r.random() for i in range(3)] for j in range(3)])

points = np.array(generate())