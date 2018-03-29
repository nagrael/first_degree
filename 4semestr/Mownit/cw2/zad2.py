from pprint import pprint


def mult_matrix(M, N):
    # Nested list comprehension to calculate matrix multiplication
    return  [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*N)] for X_row in M]

def pivot_matrix(M):
    m = len(M)

    # Create an identity matrix, with floating point values
    id_mat = [[float(i==j) for i in range(m)] for j in range(m)]
    # Rearrange the identity matrix such that the largest element of
    # each column of M is placed on the diagonal of of M
    for j in range(m):
        row = max(range(j, m), key=lambda i: abs(M[i][j]))
        if j != row:
            # Swap the rows
            id_mat[j], id_mat[row] = id_mat[row], id_mat[j]

    return id_mat

def lu_decomposition(A):
    n = len(A)
    # Create zero matrices for L and U
    L = [[0.0] * n for i in range(n)]
    U = [[0.0] * n for i in range(n)]
    # Create the pivot matrix P and the multipled matrix PA
    P = pivot_matrix(A)
    PA = mult_matrix(P, A)
    # Perform the LU Decomposition
    for j in range(n):
        # All diagonal entries of L are set to unity
        L[j][j] = 1.0
    for j in range(n):
        # LaTeX: u_{ij} = a_{ij} - \sum_{k=1}^{i-1} u_{kj} l_{ik}
        for i in range(j+1):
            s1 = sum(U[k][j] * L[i][k] for k in range(i))
            U[i][j] = PA[i][j] - s1

        # LaTeX: l_{ij} = \frac{1}{u_{jj}} (a_{ij} - \sum_{k=1}^{j-1} u_{kj} l_{ik} )
        for i in range(j, n):
            s2 = sum(U[k][j] * L[i][k] for k in range(j))
            L[i][j] = (PA[i][j] - s2) / U[j][j]

    return (P, L, U)


A = [[7, 3, -1, 2], [3, 8, 1, -4], [-1, 1, 4, -1], [2, -4, -1, 6]]
P, L, U = lu_decomposition(A)

print( "A:")
pprint(A)

print( "P:")
pprint(P)

print ("L:")
pprint(L)

print ("U:")
pprint(U)