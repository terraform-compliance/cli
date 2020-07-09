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

__Please note that__, nofail and noskip tags can not be used within the same scenario.