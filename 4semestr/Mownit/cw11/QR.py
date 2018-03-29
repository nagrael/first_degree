import numpy as np


def gram_schmidt(A):
    m, n = np.shape(A)
    k = min(n,m)
    Q = np.zeros((m, k))
    R = np.zeros((k, n))

    for j in range(n):

        v = A[:, j]
        for i in range(j):
            R[i, j] = Q[:, i].T * A[:, j]

            v = v.squeeze() - (R[i, j] * Q[:, i])

        R[j, j] = np.linalg.norm(v)
        Q[:, j] = (v / R[j, j]).squeeze()

    return Q, R
#test = np.matrix([[3.0, 1.0], [2.0, 2.0], [4.0, 5.0]])
for x in range(10,50,10):
    test = np.matrix(np.random.random((x,x)))
    Q, R= gram_schmidt(test)
    print(str((Q.dot(R)).shape))
    Q, R= np.linalg.qr(test)
    print(str((Q.dot(R)).shape))