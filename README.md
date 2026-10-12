# QCBM Ansatz Benchmark

Scripts, datasets, experiment results, and notebooks for comparing Quantum Circuit Born Machine (QCBM) ansatzes on Ising-model datasets. The project includes training, expressibility analysis, and fidelity, rate, and coverage (FRC) evaluation.

## Project contents

- [src/circuits/](src/circuits/): four circuit ansatzes and their shared specifications.
- [src/train/](src/train/): QCBM training and MMD-based objectives.
- [src/evaluation/](src/evaluation/): FRC and expressibility analysis.
- [data_2d/](data_2d/): 8- and 12-qubit training, test, and unseen datasets.
- [data/results/](data/results/): saved parameters, gradients, losses, and metrics.
- [data/expressibility/](data/expressibility/) and [graph/](graph/): analysis outputs and figures.

The saved training trajectories include large NumPy files, so cloning downloads several hundred megabytes.

## Environment

[environment.yml](environment.yml) records the original Linux/CUDA Conda environment, including JAX and PennyLane. It is a machine-specific snapshot: review its local `prefix`, CUDA package versions, and duplicate Git dependency before using it on another machine. GPU training requires a working NVIDIA driver and GPU-enabled JAX installation.

## Training

Run commands from the repository root after preparing the environment:

```bash
python src/train/gpu_train.py --ansatz 1
```

Select the circuit using `--ansatz`:

| ID | Circuit |
| --- | --- |
| 1 | `hardware_efficient_ansatz` |
| 2 | `ising_structured_ansatz` |
| 3 | `eh2d_ansatz` |
| 4 | `mi_ansatz` |

The current GPU entry point uses the 8-qubit configuration. Training writes to `data/results/Qubits8/resultN/`, where `N` is the ansatz ID; back up existing results before rerunning.

## Evaluation

Evaluate FRC from the saved 8-qubit results and render the comparison:

```bash
python src/evaluation/FRC.py
python src/evaluation/plot_frc.py
```

These commands update the saved metrics and FRC figure. For expressibility analysis:

```bash
python src/evaluation/FP2.py --ansatz 1 2 3 4 --mi-csv data_2d/Qubits8/train.csv
```

## Exploratory notebooks

[src/train/train_processes.ipynb](src/train/train_processes.ipynb), [src/train/evaluation.ipynb](src/train/evaluation.ipynb), and the plotting notebooks preserve earlier experiments. Check their dataset paths, qubit counts, and imports before running cells. Some analysis scripts, including `graph/compare.py`, contain machine-specific paths.

## Source and license

The research code and artifacts were imported from [qcbm-ansatz-benchmark](https://github.com/cxMoonGlade/qcbm-ansatz-benchmark) at commit [18dfea4](https://github.com/cxMoonGlade/qcbm-ansatz-benchmark/commit/18dfea40f2c266aba381b3b902ccfa397eb9debe). The original [MIT license and attribution](LICENSE) are retained.
