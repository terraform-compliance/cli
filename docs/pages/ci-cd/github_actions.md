---
layout: default
title: GitHub Actions
nav_order: 2
has_children: false
parent: Using in CI/CD
---

# GitHub Actions

For this example, we'll use the following GitHub Marketplace Actions to illustrate how you might implement Terraform 
Compliance into your CI/CD pipeline.

## Workflow

We have set up our job to follow this basic workflow:

1. `terraform init`
2. `terraform validate`
3. `terraform plan`
4. `terraform-compliance`
5. `terraform apply` (but only on the `main` branch)

## Setup

You will need to add a `requirements.txt` to your project. You can rename this file to anything you would like, but
be sure to update the name in your `.github/workflows/main.yml`.

Following [Pip requirements format](https://pip.pypa.io/en/stable/reference/requirements-file-format/). You can specify
any level of requirement that you desire for `terraform-compliance`.

`requirements.txt`:

```
terraform-compliance >= 1.3.0
```

Below is an example of the workflow described above.

`.github/workflows/main.yml`:

```yaml
name: Project Name

# https://docs.github.com/en/actions/using-workflows/triggering-a-workflow for available triggers
on:
  # Run this workflow on all pull requests
  pull_request:
  # Run this workflow on commits made to the main branch 
  push:
    branches:
      - main

jobs:
  test_and_deploy:
    name: Deploy Infrastructure
    runs-on: ubuntu-latest
    # Required by aws-actions/configure-aws-credentials
    permissions:
      id-token: write
      contents: read

    steps:
      # Checkout your code
      - uses: actions/checkout@v4

      # Set up our AWS credentials
      - name: Configure AWS credentials
        # https://github.com/aws-actions/configure-aws-credentials for available versions
        uses: aws-actions/configure-aws-credentials@v4
        with:
          # Define authentication method
          # Check the above repo for authentication methods available

      # Set up Terraform for GitHub Actions
      - name: Setup Terraform
        # https://github.com/hashicorp/setup-terraform for available versions
        uses: hashicorp/setup-terraform@v2
        with:
          # https://hub.docker.com/r/hashicorp/terraform/tags for available versions
          # If you also run Terraform locally, then you should use the same version here
          terraform_version: 1.5.7

      - name: Terraform Init
        run: terraform init

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        # Run terraform plan with an output, and then convert that output to JSON for Terraform Compliance to use later
        run: |
          terraform plan -out=plan.out
          terraform show -json plan.out > plan.out.json

      # Set up Python
      - name: Install Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
          cache: 'pip'

      # Install Python requirements
      - name: Install Requirements
        # Update requirements.txt to match the location of your requirements file. This is currently referencing a
        # file in the root of your project
        run: pip install -r requirements.txt

      - name: Terraform Compliance
        run: terraform-compliance -f compliance -p plan.out.json

      - name: Terraform Apply
        # Only trigger this step on the main branch
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve

```