from numpy import matrix, linalg
from numpy import random


def dominate_value(mx :matrix):
    a = 0
    x1 = matrix(random.rand(mx.shape[0], 1))
    x2 = matrix([[0] for x in range(mx.shape[0])])
    while abs(linalg.norm(x1 - x2)) > 0.0000001:
        a +=1
        x2 = x1
        x1 = mx.dot(x1)
        x1 = x1/max(x1, key=abs)
    print(x1/linalg.norm(x1))
    print(a)

