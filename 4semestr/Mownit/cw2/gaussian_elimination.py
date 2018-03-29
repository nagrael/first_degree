

def gauss(A, x):
    n = len(A)

    for i in range(0, n):
        # Search for maximum in this column
        maxEl = abs(A[i][i])
        maxRow = i
        for k in range(i+1, n):
            if abs(A[k][i]) > maxEl:
                maxEl = abs(A[k][i])
                maxRow = k

        # Swap maximum row with current row (column by column)
        for k in range(i, n):
            A[maxRow][k], A[i][k] = A[i][k], A[maxRow][k]
        x[maxRow],x[i] = x[i], x[maxRow]
        divider = A[i][i]
        for k in range(i, n):
            A[i][k] = A[i][k]/divider

        x[i] = x[i]/divider
        for j in range(i+1,n):
            mult = A[j][i]
            for k in range(i,n):
                A[j][k] = A[j][k] - mult*A[i][k]
            x[j] = x[j] - mult*x[i]
    # Solve equation Ax=b for an upper triangular matrix A
    b = [x[i]/A[i][i] for i in range(n)]
    for i in range(n-1, -1, -1):
        sums = sum(A[i][j]*b[j] for j in range(i+1,n))
        b[i] = (x[i]- sums)/A[i][i]
    return b