## [Unreleased]
### Added
- `build_ising_hamiltonian_gpu`: Enhanced to support periodic boundary conditions, long-range interactions, and disorder fields for generating physically diverse 1D Ising model Hamiltonians.
- Included optional `seed` parameter to enable reproducibility for disorder realizations.

### Motivation
This update enables more physically meaningful dataset generation for quantum thermal state modeling. Based on current literature:
- **Periodic boundaries** remove edge effects and allow simulation of bulk physics (He & Guo, 2017).
- **Long-range couplings** introduce richer entanglement structure and alter critical behavior (Gonzalez Lazo et al., 2021).
- **Disorder fields** allow modeling of Griffiths effects and broaden the training distribution for machine learning generalization (Rende et al., 2025).

These changes are foundational for generating coarse-grained, structurally valid quantum states for QCBM-based or dissipative VQA state generators.

---

## [0.1.0] - Initial Commit
### Added
- Project structure scaffolded: `data-generation`: `scripts`, `tests`, `cuq`, `utils`
- Implemented softmax-based thermal state constructor
- YAML-based parameter sweeps
- Logging and entropy/trace reporting

