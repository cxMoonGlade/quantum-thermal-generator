# quantum-thermal-generator

This repository builds toward a learned generator for approximate quantum thermal states of Ising-like systems. The goal is to produce coarse but structurally faithful mixed quantum states (e.g., Gibbs-like) that generalize across parameter space, suitable for warm-starting dissipative quantum algorithms or QGSP frameworks.

## 🧱 Current Stage: Data Generation

- Generates full-rank or top-k softmax thermal density matrices from the 1D Ising model
- Sweeps parameters: temperature (T), coupling (J), and field (h)
- Outputs `.npy` files containing trace-1, Hermitian \( \rho \)

## 🚧 Upcoming Stages

- Training a QCBM- or VQA-based generator conditioned on (T, J, h)
- Enforcing modal structure and energy-matching during learning
- Designing losses for phase-transition stability and generalization

## 🧠 Final Goal

A parameterized, generalizable generator \( f_{\theta}(T, J, h) \mapsto \tilde{\rho} \) that approximates Gibbs states well enough for warm-up or hybrid usage.
