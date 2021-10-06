---
layout: default
title: Tags
nav_order: 1
has_children: false
parent: Examples
---

# Examples about tags

AWS
{: .label .label-yellow } 

* Table of Contents
{:toc}

## Ensure all resources have tags
```gherkin
  Scenario: Ensure all resources have tags
    Given I have resource that supports tags defined
    Then it must contain tags
    And its value must not be null
```

## Ensure all resources have the whitelist tag
```gherkin
  Scenario: Ensure all resources have the whitelist tag
    Given I have resource that supports tags defined
    Then it must contain tags
    And its value must contain whitelist
```

## Ensure that specific tags are defined
```gherkin
  Scenario Outline: Ensure that specific tags are defined
    Given I have resource that supports tags defined
    When it has tags
    Then it must contain tags
    Then it must contain "<tags>"
    And its value must match the "<value>" regex

    Examples:
      | tags        | value              |
      | Name        | .+                 |
      | application | .+                 |
      | role        | .+                 |
      | environment | ^(prod\|uat\|dev)$ |
```

## Ensure that specific tags are defined for the tags_all attribute
### https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/resource-tagging#propagating-tags-to-all-resources
```gherkin
  Scenario Outline: Ensure that specific tags are defined
    Given I have resource that supports tags_all defined
    When it has tags_all
    Then it must contain tags_all
    Then it must contain "<tags>"
    And its value must match the "<value>" regex

    Examples:
      | tags        | value              |
      | Name        | .+                 |
      | application | .+                 |
      | role        | .+                 |
      | environment | ^(prod\|uat\|dev)$ |
```
