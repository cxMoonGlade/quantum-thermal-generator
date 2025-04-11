import cupy as cp

def generate_softmax_rho(H, T=1.0, top_k=20):
    evals, evecs = cp.linalg.eigh(H)
    beta = 1.0 / T
    weights = cp.exp(-beta * evals[:top_k])
    weights /= cp.sum(weights)

    rho = cp.zeros((H.shape[0], H.shape[1]), dtype=cp.complex128)
    for i in range(top_k):
        vec = evecs[:, i].reshape(-1, 1)
        rho += weights[i] * vec @ vec.conj().T

    return rho
