def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        return "Error: Incompatible matrix dimensions for multiplication."
    
    # Initializing zero matrix
    result = []
    for _ in range(rows_A):
        row = [0] * cols_B
        result.append(row)  # list of zero matrix 

    # Multiplication 
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result

A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]

result = matrix_multiply(A, B)
for row in result:
    print(row)
