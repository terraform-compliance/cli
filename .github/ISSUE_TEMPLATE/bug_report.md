---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: eerkunt

---

**Description :**
<A clear and concise description of what the bug is.>

**To Reproduce**
1. <Either a sample `terraform` code, or your `terraform plan` file if it doesn't have any confidential information>
```hcl
resource "aws_s3_bucket" "example_code" {
   bucket = "This is just a sample code"
}
```
2. <Used `terraform-compliance` parameters>
3. <Indication about either run via docker container or python package>
4. <Error output>
5. <Your feature/scenario/steps>
```gherkin
Given I have ....
When it contains ...
Then it must ....
And it must ...
```

**Expected behavior :**
<A clear and concise description of what you expected to happen.>

**Tested versions :**
- <terraform-compliance version (`terraform-compliance -v`)>
- <terraform version (`terraform -v`)>
- <python runtime version, if running as a python package (`python --version`)>

**Additional context**
Add any other context about the problem here.
