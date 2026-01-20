import numpy as np
from scipy.linalg import solve_triangular


def determinant_nxn(M):
    n_rows, n_cols = M.shape
    if M.ndim != 2:
        raise ValueError("Matrix must be 2D")
    if n_rows != n_cols:
        raise ValueError("Matrix must be square")
    if n_rows == 0:
        raise ValueError("Input must not be empty")

    det = np.linalg.det(M)
    return det
    
def inverse_matrix(M):
    n_rows, n_cols = M.shape
    if M.ndim != 2:
        raise ValueError("Matrix must be 2D")
    if n_rows != n_cols:
        raise ValueError("Matrix must be square")
    if n_rows == 0:
        raise ValueError("Input must not be empty")

    try:
        inverse = np.linalg.inv(M)
        return inverse
    except np.linalg.LinAlgError:
        return np.linalg.LinAlgError("Matrix is singular and cannot be inverted.")

def solve_system(A, b):
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
    except Exception as e:
      raise TypeError(f"Inputs A and b must be convertible to NumPy arrays: {e}")

    n_rows, n_cols = A.shape
    if A.ndim != 2:
      raise ValueError("Coefficient Matrix A must be 2D")
    if n_rows != n_cols:
      raise ValueError("Coefficient Matrix A must be square")
    if n_rows == 0:
      raise ValueError("Coefficient input A cannot be empt")

    if b.ndim != 1:
        if b.ndim == 2 and (b.shape[0] == 1 or b.shape[1] == 1):
            b = b.flatten()
        else:
            raise ValueError("Constant vector b must be 1D or a single row/column.")
    if b.shape[0] != n_rows:
         raise ValueError(f"Dimension mismatch: A has {n_rows} rows but b has {b.shape[0]} elements.")

    try:
      x = np.linalg.solve(A, b)
      return x
    except np.linalg.LinAlgError:
      raise np.linalg.LinAlgError("Matrix A is singular; system may have no unique solution.")

matrix = np.array([[3,1],[7,4]])
print(solve_system(matrix, [2,5]))

matrix_4x4 = [[4,8,4,0],[1,5,4,-3],[1,4,7,2],[1,3,0,-2]]
print(solve_system(matrix_4x4, [8,-4,10,-4]))


#triangular matrix
A_upper = np.array([[2., 4., -6.],
                    [0., 3.,  6.],
                    [0., 0.,  3.]])
b = np.array([-4., 12., 3.])
x_scipy = solve_triangular(A_upper, b, lower=False)
print(f"Solution using scipy.linalg.solve_triangular: {x_scipy}")
x_numpy = np.linalg.solve(A_upper, b)
print(f"Solution using numpy.linalg.solve: {x_numpy}")