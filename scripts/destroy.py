#!/usr/bin/env python3
"""
destroy.py

Reads the same YAML config and tears down all infrastructure.
"""

import argparse
import subprocess
import sys
import yaml
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Destroy GCP infra via Terraform"
    )
    parser.add_argument(
        "config", type=Path,
        help="Path to the same YAML config you used to deploy"
    )
    return parser.parse_args()

def yaml_to_tfvars(config_path: Path, tfvars_path: Path):
    logger.info(f"Loading YAML config from {config_path}")
    data = yaml.safe_load(config_path.read_text())
    lines = []
    for k, v in data.items():
        if isinstance(v, dict):
            lines.append(f"{k} = {{")
            for kk, vv in v.items():
                lines.append(f'  {kk} = "{vv}"')
            lines.append("}")
        elif isinstance(v, list):
            lines.append(f"{k} = [")
            for item in v:
                lines.append(f'  "{item}",')
            lines.append("]")
        else:
            lines.append(f'{k} = "{v}"')
    tfvars_path.write_text("\n".join(lines))
    logger.info(f"Wrote Terraform var‑file to {tfvars_path}")

def run_cmd(cmd):
    logger.info(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)

def main():
    args = parse_args()
    tfvars = Path.cwd() / "config.auto.tfvars"

    try:
        yaml_to_tfvars(args.config, tfvars)
        run_cmd(["terraform", "init"])
        run_cmd(["terraform", "destroy", "-auto-approve"])
    except subprocess.CalledProcessError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
