# /data-generation/scripts/generate_dataset.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import yaml
import cupy as cp
import numpy as np
import json
import itertools
import logging
from utils.hamiltonian import build_ising_hamiltonian_gpu
from cuq.thermal_constructor import generate_softmax_rho

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
LOG_PATH = os.path.join(os.path.dirname(__file__), "../generation.log")

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def save_density_matrix(rho, metadata, outdir=DATA_DIR):
    os.makedirs(outdir, exist_ok=True)
    fname = f"rho_n{metadata['n']}_T{metadata['T']:.2f}_J{metadata['J']:.2f}_h{metadata['h']:.3f}.npy"
    path = os.path.join(outdir, fname)
    np.save(path, cp.asnumpy(rho))
    with open(path.replace(".npy", ".json"), "w") as f:
        json.dump(metadata, f, indent=2)
    logging.info(f"Saved: {fname} (trace={metadata['trace']:.5f}, entropy={metadata['entropy']:.5f})")

def main():
    try:
        with open("config/params.yaml", "r") as f:
            cfg = yaml.safe_load(f)["sweep"]
    except Exception as e:
        logging.error(f"Failed to read YAML config: {e}")
        return

    sweep_keys = [k for k in cfg if isinstance(cfg[k], list)]
    sweep_values = [cfg[k] for k in sweep_keys]
    static_cfg = {k: cfg[k] for k in cfg if not isinstance(cfg[k], list)}

    if not sweep_keys:
        logging.warning("No sweep parameters found. Nothing to generate.")
        return

    total, success, failure = 0, 0, 0

    for vals in itertools.product(*sweep_values):
        total += 1
        params = dict(zip(sweep_keys, vals))
        run_cfg = {**static_cfg, **params}
        logging.info(f"Generating config: {run_cfg}")

        try:
            ham_args = {k: run_cfg[k] for k in ['n', 'J', 'h', 'periodic', 'long_range', 'disorder', 'seed']}
            H = build_ising_hamiltonian_gpu(**ham_args)
            rho = generate_softmax_rho(H, T=run_cfg["T"], top_k=run_cfg["top_k"])

            trace = cp.trace(rho).real.item()
            entropy = -cp.trace(rho @ cp.log(rho + 1e-10)).real.item()

            metadata = run_cfg.copy()
            metadata.update({"trace": trace, "entropy": entropy})

            save_density_matrix(rho, metadata)
            success += 1
        except Exception as e:
            logging.error(f"Failed to generate data for config {run_cfg}: {e}")
            failure += 1

    logging.info(f"Generation completed. Total: {total}, Success: {success}, Failure: {failure}")

if __name__ == "__main__":
    main()
