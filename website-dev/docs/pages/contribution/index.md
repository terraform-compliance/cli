---
layout: default
title: Contributing
nav_order: 7
has_children: false
---

# Contributing to terraform-compliance

**First**: if you're unsure or afraid of anything, just ask or submit the issue or pull request anyways. 
You won't be yelled at for giving your best effort. The worst that can happen is that you'll be politely 
asked to change something. We appreciate any sort of contributions, and don't want a wall of rules to get 
in the way of that.

However, for those individuals who want a bit more guidance on the best way to contribute to the project, 
read on. This document will cover what we're looking for. By addressing all the points we're looking for, 
it raises the chances we can quickly merge or address your contributions.

## Reporting an Issue

Currently `terraform-compliance` supports 3 types of issue types ;

- [Bug Reporting](https://github.com/eerkunt/terraform-compliance/issues/new?assignees=eerkunt&labels=bug&template=bug_report.md&title=)
- [Feature Request](https://github.com/eerkunt/terraform-compliance/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=)
- [General Question](https://github.com/eerkunt/terraform-compliance/issues/new?assignees=&labels=&template=general-question.md&title=)

If you are going to reporting something else, please create a [General Question](https://github.com/eerkunt/terraform-compliance/issues/new?assignees=&labels=&template=general-question.md&title=) issue.

## Pull Request Process

Normally, we expect to have either a [Bug Reporting](https://github.com/eerkunt/terraform-compliance/issues/new?assignees=eerkunt&labels=bug&template=bug_report.md&title=) or 
a [Feature Request](https://github.com/eerkunt/terraform-compliance/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=) before 
having a Pull Request for in the codebase that will effect any functionality. This is not a hard requirement, you are free
to create a new Pull Request if you find something is wrong or missing within the codebase or documentation. 

There is few mandatory requirement for the Pull Requests ;

1. All code changes that effects functionality MUST have [tests](https://github.com/eerkunt/terraform-compliance/tree/master/tests) implemented within the same Pull Request. 
2. Any functionality change must be recorded within the [CHANGELOG](https://github.com/eerkunt/terraform-compliance/blob/master/CHANGELOG.md).
3. Your Pull Request must pass the CI in order to be processed.

Usually, Pull Requests are being processed within the same day, worst case your PR will wait for 1-2 days.

## Code Structure

```
.
├── terraform_compliance
│   ├── common
│   ├── extensions
│   └── steps
├── docs
│   └── pages
│       ├── Examples
│       ├── bdd-references
│       ├── contribution
│       ├── installation
│       ├── usage
│       └── using-in-a-pipeline
└── tests
    └── terraform_compliance
        ├── common
        ├── extensions
        └── steps
```

All functionality defined in `terraform_compliance` directory where all test defined on `tests` with the same structure. So if you
change something in the `terraform_compliance/steps`, then the tests must exist in `tests/steps`.

`terraform-compliance` uses [radish](http://radish-bdd.io/) for the BDD framework, with lots of [extensions](https://github.com/eerkunt/terraform-compliance/tree/master/terraform_compliance/extensions) written to parse and process 
terraform files. Most of the functionality is described in https://terraform-compliance.com. 

## How to write tests

You will usually want to only write functional tests. 

Structure

```
.
├── terraform_compliance
│  
├── docs
│
└── tests
    └── terraform_compliance (unit tests)
    └── functional (integration tests)
        ├── ...
        └── your_test_directory
            ├── main.tf
	        ├── plan.out.json
	        ├── test.feature
	        └── Dotfiles (optional)
```

### Dotfiles

All dotfiles are optional.

* .failure
	- if this file exists, the test will be expected to fail
* .expected
	- Expected output. The tests will fail if scenarios in test.feature won't produce every line (output) in .expected. A common use case is to check if a specific error happens in the test.
* .unexpected
	- Unexpected output. Similar to .expected, but the test fails if any of the tests produces any of the lines in .unexpected

### Test your changes
`tox -e unit` to runs unit tests <br>
`tox -e integration` to runs integration tests

## Updating Website

`terraform-compliance` uses Jekyll for templating and Github Pages for serving its website. https://terraform-compliance.com

Website is stored in [docs](https://github.com/eerkunt/terraform-compliance/tree/master/docs) directory, where in most cases changes in [docs/pages](https://github.com/eerkunt/terraform-compliance/tree/master/docs/pages) will be sufficient for adding/removing/updating website pages. 

## Release Cycle

Usually after every functionality change we try to release a new package immediately. 


 
