# terraform-wrapper-aws

Terraform wrapper script that gets AWS credentials and region from environment variables and starts deploying the infrastructure. If the corresponding variables are not set, the script will get their values from `ENV_FILE` passed as a command line argument.

## Usage

`tf-wrapper-aws.py [-h] [-d TERRAFORM_DIR] [-f ENV_FILE]`

## Options

- `-h`, `--help`:

  Show this help message and exit.

- `-d TERRAFORM_DIR`, `--directory TERRAFORM_DIR`:

  Directory containing Terraform configuration files (default: current directory).

- `-f ENV_FILE`, `--env-file ENV_FILE`:

  File containing missing environment variables. If the file contains a variable that is already
  set in the system, the script will not override its value (default: `TERRAFORM_DIR/.env`).
