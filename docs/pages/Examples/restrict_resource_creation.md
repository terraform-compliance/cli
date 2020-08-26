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
@noskip
Scenario: Ensure some resource types are always created (with Given)
	Given I have some_resource_type defined


@noskip_at_line_9
Scenario: Ensure some resource types are always created (with When)
	Given I have any resource defined
	When its type is some_resource_type  # line 9
```