#!/usr/bin/env python3

import argparse
import subprocess
import sys
import yaml
from pathlib import Path

# ---------------------------------------------------------------------------- #
#                               Helper Functions                               #
# ---------------------------------------------------------------------------- #

def log(msg: str, level: str = "INFO"):
    print(f"[{level}] {msg}")

def run(cmd: list, cwd: Path = None) -> bool:
    """Run a subprocess command, stream stdout/stderr, return success."""
    log(f"Running: {' '.join(cmd)}")
    try:
        completed = subprocess.run(
            cmd, cwd=cwd, check=True, text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        log(f"Command failed (exit {e.returncode}): {' '.join(cmd)}", level="ERROR")
        return False

def yaml_to_tfvars(yaml_path: Path, tfvars_path: Path):
    """Convert a flat YAML map to terraform.tfvars format."""
    data = yaml.safe_load(yaml_path.read_text())
    lines = []
    for k, v in data.items():
        # skip empty or null
        if v is None:
            continue
        # strings, numbers, bools
        if isinstance(v, (str, int, float, bool)):
            val = f'"{v}"' if isinstance(v, str) else str(v).lower()
            lines.append(f'{k} = {val}')
        # lists
        elif isinstance(v, list):
            items = []
            for item in v:
                if isinstance(item, str):
                    items.append(f'"{item}"')
                else:
                    items.append(str(item))
            lines.append(f'{k} = [{", ".join(items)}]')
        # maps
        elif isinstance(v, dict):
            lines.append(f'{k} = {{')
            for kk, vv in v.items():
                val = f'"{vv}"' if isinstance(vv, str) else str(vv).lower()
                lines.append(f'  {kk} = {val}')
            lines.append('}')
        else:
            log(f"Skipping unsupported type for key {k}: {type(v)}", level="WARN")

    tfvars_path.write_text("\n".join(lines) + "\n")
    log(f"Wrote {tfvars_path.name} with {len(lines)} entries")

# ---------------------------------------------------------------------------- #
#                              Main Workflow Logic                             #
# ---------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(
        description="Deploy or destroy Terraform infra from a YAML config"
    )
    parser.add_argument("config", type=Path, help="Path to your YAML config file")
    parser.add_argument(
        "-w", "--workspace", default="default",
        help="Terraform workspace to use (will be created if needed)"
    )
    parser.add_argument(
        "--plan-only", action="store_true",
        help="Only run terraform plan, do not apply"
    )
    parser.add_argument(
        "--destroy", action="store_true",
        help="Run terraform destroy instead of apply"
    )
    parser.add_argument(
        "-a", "--auto-approve", action="store_true",
        help="Pass -auto-approve to apply/destroy"
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.resolve()
    tfvars = repo_root / "terraform.tfvars"

    # 1) Validate YAML exists
    if not args.config.exists():
        log(f"Config file not found: {args.config}", level="ERROR")
        sys.exit(1)

    # 2) Convert YAML → terraform.tfvars (preserving any existing alphanumeric order)
    yaml_to_tfvars(args.config, tfvars)

    # 3) Initialize & select workspace
    if not run(["terraform", "init"], cwd=repo_root):
        sys.exit(1)

    # Create or select workspace
    run(["terraform", "workspace", "new", args.workspace], cwd=repo_root)  # ignore errors
    if not run(["terraform", "workspace", "select", args.workspace], cwd=repo_root):
        sys.exit(1)

    # 4) Plan
    plan_cmd = ["terraform", "plan", "-var-file=terraform.tfvars"]
    if not run(plan_cmd, cwd=repo_root):
        sys.exit(1)

    if args.plan_only:
        log("Plan-only mode, exiting without apply/destroy")
        sys.exit(0)

    # 5) Apply or Destroy
    action = "destroy" if args.destroy else "apply"
    cmd = ["terraform", action, "-var-file=terraform.tfvars"]
    if args.auto_approve:
        cmd.append("-auto-approve")

    if not run(cmd, cwd=repo_root):
        sys.exit(1)

    log(f"Terraform {action} completed successfully! 🎉")
    

    # 6) Update last deployed config if not a destroy
    last_config_path = repo_root / ".last_deployed_config"
    if not args.destroy:
        last_config_path.write_text(str(args.config.resolve()))
        log(f"Updated .last_deployed_config with: {args.config}")

    sys.exit(0)
if __name__ == "__main__":
    main()
