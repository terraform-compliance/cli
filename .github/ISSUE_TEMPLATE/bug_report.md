---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: eerkunt

---

<!-- Thank you for opening an issue! -->
## Description
<!-- A clear and concise description of what the bug is. -->

## To Reproduce
<!--
To fix problems, we usually only need the following:
   1. Feature/Scenarios/Steps you are running terraform-compliance with
   2. plan.out.json file you are running terraform-compliance against

More context can only help:
   3. Sample `terraform` code that generates parts or the entirety of the shared terraform plan
   4. Used `terraform-compliance` parameters
   5. Indication about either run via docker container or python package
   6. Error output


Providing a plan file makes it x10 times easier to reproduce your problem. Sometimes, it can be difficult to provide an anonymized version of the plan file. In those cases, sharing the terraform code will suffice. 

However, difficulty in reproducing the issue makes it more difficult to get to it. If you are not sharing a plan file and your setup involves using multiple files, directories, variables, or modules, please share more information on how to reproduce it. This may include:
- Overview of your file structure
- Mock variable files
- Instructions on how to compile the files you provided
-->

**Feature File**
<!-- Can link to the file or paste it below-->
```gherkin
Given I have ....
When it contains ...
Then it must ....
And it must ...
```
**Plan File**
<!-- Please make sure that your plan doesn't have any confidential information. -->

**Sample Terraform Code**
<!-- Can link to the file or paste it below. Please make sure that your code doesn't have any confidential information. -->
```hcl
resource "aws_s3_bucket" "example_code" {
   bucket = "This is just a sample code"
}
```

**Used `terraform-compliance` parameters**
<!-- If anything other than `-p` and `-f` is being used, please let us know. -->

**Running via Docker**
<!-- Yes or No -->
<!-- If not running via Docker, this section can be deleted. Otherwise, docker related information goes here. -->

**Error Output**
<!-- What did happen? -->

**Expected behavior:**
<!-- What did you expect to happen? -->

**Tested versions:**
- terraform-compliance version: ```your terraform-compliance version``` <!-- terraform-compliance -v -->
- terraform version: ```your terraform version``` <!-- terraform -v -->
- python version: ```your python runtime version, if running as a python package``` <!-- python -v -->

**Additional context**
<!-- Add any other context about the problem here. -->
