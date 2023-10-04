---
layout: default
title: Using Tags
nav_order: 7
has_children: true
parent: BDD Reference
---

# Using Tags

`terraform-compliance` supports using tags within the BDD feature files.

An example tag usage :
```gherkin
Feature: My test feature

@nofail
Scenario: #1 Ensure my specific s3 buckets are private but dont fail
  Given I have aws_s3_bucket defined
  Then it must contain acl
  And its value must be private

Scenario: #2 Some other scenario that may fail
  Given ....
  ...
```

in this case, `terraform-compliance` will execute both scenarios but will never
fail Scenario #1 due to `@nofail` tag. These tags can also be use on top of the
Features instead of Scenarios. Default `Failure :` error heading will also be changed
with the tag name. It will be `nofail :` in the example above.

## Supported Tags

| Tag Name(s) | Description |
|:-----------:|:------------|
| `warning`, `no-failure`, `no-fail`, `info`, `nofailure`, `nofail`, `dontfail` | Do not fail the scenario. |
| `noskip`, `no-skip`, `dontskip`, `failonskip`, `fail-on-skip` | Fail if any part of the scenario skips. |
| `noskip_at_line_8`, `no-skip_at_lines_10_22_23`,  | Fail if any of the indicated lines skips. __Note:__ only GIVEN and WHEN steps can be skipped |
| `case-sensitive`, `case_sensitive`, `case-sensitivity`, `casesensitive` | Use case sensitive matching on all steps. (Including regexes)|
| `exclude_aws_s3_bucket.mybucket`, `ignore_azurerm_storage_account.example`, `exclude_resource_type.resource_name` | Exclude given resource from this scenario.|

__Please note that__, nofail and noskip tags can not be used within the same scenario.

## Reference
* Table of Contents
{:toc}

### Warning
This tag converts failing scenarios to warnings. Warnings will not be considered as skipped steps and will not change the return code of terraform-compliance.

> __Possible formats:__
>
> ▪
warning, no-failure, no-fail, info, nofailure, nofail, dontfail
>

__Please note that__
- nofail and noskip tags can not be used within the same scenario.

### Noskip
In Terraform-Compliance, `WHEN` always filters and `THEN` always drills down. However, this might not always be the desired behavior. With `noskip`, conditions can be forced without having to drill down to their values.

`@noskip` fails the scenario if any of the steps skips. Using `@noskip_at_lines_2_3`, will fail if there are skipping steps within the scenario that falls into the lines 2 and 3

`@noskip` fails all the skipping scenarios produced from a scenario outline. Using `@noskip_at_line_2` will fail a skipping scenario that was produced from a scenario outline with using the examples on line 2.

> __Possible formats:__
>
> ▪
noskip, no-skip, dontskip, failonskip, fail-on-skip
>
> ▪
noskip_at_line_8
>
> ▪
no-skip_at_lines_10_22_23
>

__Please note that__
- nofail and noskip tags can not be used within the same scenario.

### Case Sensitivity
All steps, under the tagged scenario will use case-sensitive matching. This tag also affects regular expressions.
> __Possible formats:__
>
> ▪
`case-sensitive`, `case_sensitive`, `case-sensitivity`, `casesensitive`
>

### Exclude Resources
`exclude` tag prevents the resource or resources described by the following regular expression to be ignored by the scenario. When `@exclude_regular_expression` is used, resources with addresses that match the regex will be ignored.

> __Possible formats:__
>
> ▪
exclude_aws_s3_bucket.mybucket
>
> ▪
ignore_azurerm_storage_account.example
>
> ▪
exclude_module.ecr_repository\[\"repository_[0-9]\"\].aws_ecr_repository.ecr_repository>
>
> ▪
ignore_module.ecr_repository.*aws_ecr_repository.ecr_repository
>

__Please note that__
- The correct address format of a resource can be looked up via the debugger
- This tag does not support paranthesis, hence grouping, due to how tags are being parsed.
- Special characters such as `[` should be escaped. (`\[`)
- Using `.` or `.*` within your expression can help simplify the step greatly.
