# utils/hamiltonian.py
import cupy as cp
import numpy as np

def kron_N(ops):
    result = ops[0]
    for op in ops[1:]:
        result = cp.kron(result, op)
    return result

def build_ising_hamiltonian_gpu(n, J=1.0, h=0.0, periodic=False, long_range=False, disorder=False, seed=None):
    cp.random.seed(seed)
    I = cp.eye(2)
    Z = cp.array([[1, 0], [0, -1]])
    X = cp.array([[0, 1], [1, 0]])

    H = cp.zeros((2**n, 2**n), dtype=cp.complex128)

    for i in range(n):
        j = (i + 1) % n if periodic or i < n - 1 else None
        if j is None:
            continue

        J_ij = J + 0.1 * cp.random.randn() if disorder else J
        ops = [I] * n
        ops[i] = Z
        ops[j] = Z
        H -= J_ij * kron_N(ops)

    if long_range:
        for i in range(n):
            for j in range(i + 2, n):
                J_ij = J / abs(j - i)
                ops = [I] * n
                ops[i] = Z
                ops[j] = Z
                H -= J_ij * kron_N(ops)

    for i in range(n):
        h_i = h + 0.1 * cp.random.randn() if disorder else h
        ops = [I] * n
        ops[i] = X
        H -= h_i * kron_N(ops)

    return H