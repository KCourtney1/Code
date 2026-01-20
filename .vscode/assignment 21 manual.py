import numpy as np

def determinant_nxn(M):
    n_rows, n_cols = M.shape
    if M.ndim != 2:
        raise ValueError("Array must be 2d")
    if n_rows != n_cols:
        raise ValueError("Array must be square")
    if n_rows == 0:
        raise ValueError("Input must not be empty")

    n = n_rows
    if n == 1:
            return M[0, 0]
    
    det = 0
    for j in range(n):
        sign = (-1)**j
        element = M[0,j]

        minor = np.delete(M,0,axis=0)
        minor = np.delete(minor, j, axis=1)
        det_minor = determinant_nxn(minor)
        det += sign * element * det_minor
    return det

def inverse_matrix(M):
    n_rows, n_cols = M.shape
    if M.ndim != 2:
        raise ValueError("Array must be 2d")
    if n_rows != n_cols:
        raise ValueError("Array must be square")
    if n_rows == 0:
        raise ValueError("Input must not be empty")
    det = determinant_nxn(M)
    if np.isclose(det, 0.0):
        return np.linalg.LinAlgError("Matrix is singular and cannot be inverted.")

    n = n_rows
    if n == 1:
        return np.array([[1.0/M[0,0]]])
    
    cofactors = np.zeros_like(M, dtype=float)
    for i in range(n):
        for j in range(n):
            sign = (-1) ** (i + j)
            minor = np.delete(np.delete(M, i, axis=0), j, axis=1)
            det_minor = determinant_nxn(minor)
            cofactors[i, j] = sign * det_minor
    adjugate = cofactors.T  #transpose
    inverse = (1.0 / det) * adjugate
    return inverse

matrix = np.array([[3,1],[7,4]])
matrix_np_3x3 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
matrix_np_4x4 = np.array([[3, 2, 0, 1], [4, 0, 1, 2], [-3, 0, 2, 1], [2, 0, 1, 1]])

print(determinant_nxn(matrix))
print(determinant_nxn(matrix_np_3x3))
print(determinant_nxn(matrix_np_4x4))
print(inverse_matrix(matrix))
print(inverse_matrix(matrix_np_3x3))
print(inverse_matrix(matrix_np_4x4))