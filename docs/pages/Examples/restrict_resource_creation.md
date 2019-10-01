---
layout: default
title: Restrict Resources
nav_order: 7
has_children: false
parent: Examples
---

AWS
{: .label .label-yellow } 

* Table of Contents
{:toc}

# Examples about Restricting Resources

## Restrict creation of specific resources
```gherkin
Scenario Outline: Restrict creation of specific resources
  Given I have <resource> defined
  Then the scenario should fail

  Examples:
  | resource              |
  | AWS Security Group    |
  | aws_vpc               |
  | aws_internet_gateway  |
  | aws_ec2_instance      |
```

## Ensure some resource types are always created
```gherkin
  Scenario: Ensure some resource types are always created
    Given I have any resource defined
    When its type is not some_resource_type
    Then the scenario should fail
```