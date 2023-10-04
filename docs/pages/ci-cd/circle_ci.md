---
layout: default
title: CircleCI
nav_order: 1
has_children: false
parent: Using in CI/CD
---

# CircleCI

For this example, we are using the following Orbs to illustrate how you might implement Terraform Compliance into your
CI/CD pipeline.

- [circleci/terraform](https://circleci.com/developer/orbs/orb/circleci/terraform)
- [circleci/python](https://circleci.com/developer/orbs/orb/circleci/python)

## Workflow

We have set up our pipeline to follow this basic workflow:

1. `terraform validate`: Using the Job provided by the Terraform Orb
2. `terraform plan`: Using a custom Job, we will use the `plan` command that is provided by the Terraform Orb, but we'll also export that plan to json for `terraform-compliance` to access
3. `terraform-compliance`: Using the Python Orb and Pip to install requirements
4. `terraform apply`: Using the Job provided by the Terraform Orb, and only run on the `main` branch

## Setup

You will need to add a `requirements.txt` to your project. You can rename this file to anything you would like, but
be sure to update the name in your `.circleci/config.yml`.

Following [Pip requirements format](https://pip.pypa.io/en/stable/reference/requirements-file-format/). You can specify
any level of requirement that you desire for `terraform-compliance`.

`requirements.txt`:

```
terraform-compliance >= 1.3.0
```

Below is an example of the workflow described above.

`.circleci/config.yml`:

```yaml
version: '2.1'

orbs:
  # Orb used for all of our Terraform related commands/jobs
  # https://circleci.com/developer/orbs/orb/circleci/terraform for available versions
  terraform: circleci/terraform@3.2.1
  # Orb used for installing and running Terraform Compliance
  # https://circleci.com/developer/orbs/orb/circleci/python for available versions
  python: circleci/python@2.1.1

parameters:
  terraform-tag:
    type: string
    description: Specify the Terraform Docker image tag for the executor
    # https://hub.docker.com/r/hashicorp/terraform/tags for available versions
    # If you also run Terraform locally, then you should use the same version here
    default: 1.5.7
  workspace-root:
    type: string
    description: Path of the workspace to persist to relative to workspace-root
    # Can be updated if you desire. The default specified here matches the default used by the CircleCI's Terraform Orb
    default: .
  workspace-path:
    type: string
    description: Workspace root path that is either an absolute path or a path relative to the working directory
    # Can be updated if you desire. The default specified here matches the default used by the CircleCI's Terraform Orb
    default: .

executors:
  # This default executor is used for our custom job that needs to run Terraform
  default:
    docker:
      # Our default executor should match the tag that the Terraform Orb will use
      - image: hashicorp/terraform:<< pipeline.parameters.terraform-tag >>

jobs:
  terraform_plan:
    executor: default
    steps:
      - checkout
      # Invoke the terraform/plan command that is provided by the Terraform Orb
      - terraform/plan:
          # And also output that plan
          out: plan.out
      # Convert our plan to JSON so that terraform-compliance can run without the use of Terraform
      - run:
          command: terraform show -json plan.out > plan.out.json
          name: Convert Terraform plan to JSON
      # Persist our workspace so that plan.out.json is available to terraform-compliance
      - persist_to_workspace:
          paths:
            - << pipeline.parameters.workspace-path >>
          root: << pipeline.parameters.workspace-root >>

  terraform_compliance:
    executor: python/default
    steps:
      # Attach the workspace so that we have access to plan.out.json from terraform_plan
      - attach_workspace:
          at: << pipeline.parameters.workspace-root >>
      - python/install-packages:
          # Update requirements.txt to match the location of your requirements file. This is currently referencing a
          # file in the root of your project
          pip-dependency-file: requirements.txt
          pkg-manager: pip
      - run:
          command: terraform-compliance -f features -p plan.out.json
          name: Terraform Compliance

workflows:
  deploy_infra:
    jobs:
      # Use the standard validate job that is provided by the CircleCI Orb
      - terraform/validate:
          checkout: true
          # Make sure the CircleCI Orb uses the same version of Terraform as our default executor
          tag: << pipeline.parameters.terraform-tag >>

      # For terraform plan we'll use a custom job so that we can run additional commands
      - terraform_plan:
          requires:
            - terraform/validate

      # For terraform-compliance we'll use another custom job, and this will also be using our Python executor
      - terraform_compliance:
          requires:
            - terraform_plan

      # Use the standard apply job that is provided by the CircleCI Orb
      - terraform/apply:
          attach-workspace: true
          # Make sure the CircleCI Orb uses the same version of Terraform as our default executor
          tag: << pipeline.parameters.terraform-tag >>
          # Update your filters as you require. One provided here as an example
          filters:
            branches:
              only: main
          requires:
            - terraform_compliance

```