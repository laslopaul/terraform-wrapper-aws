#!/usr/bin/env python3

import os
import subprocess
import sys
import argparse


TERRAFORM_DIR = os.path.abspath(".")
ENV_VARS = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"]


def check_environment_variables() -> bool:
    """Check if the specified environment variables are set in the system"""
    return all(map(lambda x: os.getenv(x) is not None, ENV_VARS))


def run_terraform(directory: str) -> None:
    """Run terraform init and apply"""
    try:
        subprocess.run(["terraform", "init"], check=True, cwd=directory)
        subprocess.run(
            ["terraform", "apply", "-auto-approve"], check=True, cwd=directory
        )
    except subprocess.CalledProcessError as e:
        print("Error running Terraform: ", e)
        sys.exit(1)


def load_environment_variables(env_file: str) -> None:
    """Load missing environment variables from a file"""
    if not os.path.exists(env_file):
        print(f"{env_file}: file not found")
        sys.exit(1)
    with open(env_file) as f:
        for line in f:
            if not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()

                if not os.getenv(key) and key in ENV_VARS:
                    print(f"Setting environment variable: {key}")
                    os.environ[key] = value

    # Check if some variables are still remaining unset
    unset_vars = list(filter(lambda x: os.getenv(x) is None, ENV_VARS))
    if len(unset_vars) > 0:
        unset_vars_str = ', '.join(unset_vars)
        print(
            f"Error: unable to set the following variables: {unset_vars_str}"
        )
        exit(1)


def main() -> None:
    """Parse arguments, invoke checks and run Terraform"""
    parser = argparse.ArgumentParser(
        description="""
        Terraform wrapper script that gets AWS credentials and region
        from environment variables and starts deploying the infrastructure.
        If the corresponding variables are not set, the script will get their
        values from ENV_FILE passed as a command line argument.
        """
    )
    parser.add_argument(
        "-d",
        "--directory",
        metavar="TERRAFORM_DIR",
        default=TERRAFORM_DIR,
        help="""
        directory containing Terraform configuration files
        (default: current directory)
        """
    )
    parser.add_argument(
        "-f",
        "--env-file",
        metavar="ENV_FILE",
        help=f"""
        file containing missing environment variables.
        If the file contains a variable that is already set in the system,
        the script will not override its value.
        (default: {os.path.join('TERRAFORM_DIR', '.env')})
        """,
    )

    args = parser.parse_args()

    try:
        subprocess.run(
            ["terraform", "-version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=args.directory,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Terraform is not installed or not in PATH")
        sys.exit(1)

    if not check_environment_variables():
        default_env_file = os.path.join(args.directory, ".env")
        load_environment_variables(
            default_env_file if args.env_file is None else args.env_file
        )

    run_terraform(args.directory)


if __name__ == "__main__":
    main()
