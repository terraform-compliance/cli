<h1 align="center">terraform-compliance</h1>

<div align="center">
  <strong>BDD Testing for Terraform Files</strong>
</div>
<div align="center">
  A lightweight BDD-testing Compliance Framework 
</div>

<br />

<div align="center">
  <!-- Stability -->
    <img src="https://img.shields.io/badge/stability-experimental-orange.svg?style=flat-square"
      alt="Code Stability" />
  </a>
  <!-- Build Status -->
  <a href="https://travis-ci.org/eerkunt/terraform-compliance">
    <img src="https://img.shields.io/travis/eerkunt/terraform-compliance/master.svg?style=flat-square"
      alt="Build Status" />
  </a>
  <!-- Test Coverage -->
  <a href="https://codecov.io/github/eerkunt/terraform-compliance">
    <img src="https://img.shields.io/codecov/c/github/eerkunt/terraform-compliance/master.svg?style=flat-square"
      alt="Test Coverage" />
  </a>
  <!-- Downloads -->
  <a href="https://npmjs.org/package/choo">
    <img src="https://img.shields.io/pypi/v/terraform-compliance.svg?style=flat-square&label=version"
      alt="Downloads" />
  </a>
</div>

## Table of Contents
- [Features](#features)
- [Example](#example)
- [FAQ](#faq)
- [Installation](#installation)
- [Usage](#usage)

## Features
- __compliance:__ Test your infrastructure as code before you deploy. Enforce your people to follow the policies.
- __behaviour driven development:__ We have BDD for nearly everything, why not for IaC ?
- __fixed steps:__ fixed steps coming with the package, just focus on your BDD feature/scenario files.
- __portable:__ just install it from `pip`
- __why ?:__ why not ?

## Example
![Example Run](terraform-compliance-demo.gif)
```sh
[~] $ terraform-compliance -f example/example_01 -t example/tf_files
terraform-compliance v0.1.0 initiated
Features : /Users/sharky/Repository/terraform-compliance/example/example_01
Steps    : /Users/sharky/Repository/venv2/lib/python2.7/site-packages/terraform_compliance/steps
TF Files : /Users/sharky/Repository/terraform-compliance/example/tf_files
Validating terraform files.
All HCL files look good.
Running tests.
Feature: Security Groups should be used to protect services/instances  # /path/to/example/example_01/aws/security_groups.feature
    In order to improve security
    As engineers
    We'll use AWS Security Groups as a Perimeter Defence

    Scenario Outline: Policy Structure
        Given I define AWS Security Group
        Then it must contain <policy_name>

    Examples:
        | policy_name |
        | ingress     |
        | egress      |

    Scenario Outline: Well-known insecure protocol exposure on Public Network for ingress traffic
        Given I define AWS Security Group
        Then it must contain ingress
        with <proto> protocol and not port <portNumber> for 0.0.0.0/0

    Examples:
        | ProtocolName | proto | portNumber |
        | HTTP         | tcp   | 80         |
        | Telnet       | tcp   | 23         |
        | SSH          | tcp   | 22         |
        | MySQL        | tcp   | 3306       |
        | MSSQL        | tcp   | 1443       |
        | NetBIOS      | tcp   | 139        |
        | RDP          | tcp   | 3389       |

Feature: Subnets should be defined properly for network security  # /path/to/example/example_01/aws/subnets.feature
    In order to improve security
    And decrease impact radius
    As engineers
    We'll use a layered architecture in our AWS Environment

    Scenario: Subnet Count
        Given I define AWS Subnet
        When I count them
        Then I expect the result is more than 2
          AssertionError: 0 is not more than 2

2 features (1 passed, 1 failed)
10 scenarios (9 passed, 1 failed)
28 steps (27 passed, 1 failed)

[~] $ echo $?
1
[~] $
```

## FAQ

- __Q.__ Where are the steps defined ?
- __A.__ They all comes with `terraform-compliance`, you can just focus on BDD feature/scenario files.
<br /><br />
- __Q.__ What if I would like to add more steps ?
- __A.__ You are welcome to contribute on any test, or just add an issue it will be added.
<br /><br />
- __Q.__ Where should `terraform-compliance` run ?
- __A.__ Ideally in a CI/CD tool, where company policies are defined as feature files and all IaC is tested against. Trust, but verify.

## Installation
```sh
[~] $ pip install terraform-compliance
```

### Usage
```sh
[~] $ terraform-compliance --help
usage: terraform-compliance [-h] [--features feature_directory]
                            [--tfdir terraform_directory]

BDD Test Framework for Hashicorp terraform

optional arguments:
  -h, --help            show this help message and exit
  --features feature_directory, -f feature_directory
                        Directory consists of BDD features
  --tfdir terraform_directory, -t terraform_directory
                        Directory consists of Terraform Files
```

You can also push additional arguments that is specific for `radish`. Just to explain how it works ;

For e.g.
```sh
[~] $ terraform-compliance -f /path/to/features -t /path/to/terraform_files -v
terraform-compliance v0.1.0 initiated
Features : /Users/sharky/Repository/terraform-compliance/example/example_01
Steps    : /Users/sharky/Repository/venv2/lib/python2.7/site-packages/terraform_compliance/steps
TF Files : /Users/sharky/Repository/terraform-compliance/example/tf_files
Validating terraform files.
All HCL files look good.
Running tests.
0.8.6
```
Please note that `0.8.6` is the `radish` version comes from `-v` parameter.


## License
[MIT](https://tldrlegal.com/license/mit-license)
