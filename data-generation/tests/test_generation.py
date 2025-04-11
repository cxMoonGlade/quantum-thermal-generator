import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cupy as cp
from cuq.thermal_constructor import generate_softmax_rho

rho = generate_softmax_rho(n=8, T=1.5, J=1.0, h=0.5)
print(rho.shape)
print("Trace =", cp.trace(rho).real)
