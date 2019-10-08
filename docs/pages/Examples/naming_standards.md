---
layout: default
title: Naming Standards
nav_order: 4
has_children: false
parent: Examples
---

AWS
{: .label .label-yellow } 

* Table of Contents
{:toc}

# Examples about Naming Standards
## Naming Standard on all available resources
```gherkin
  Scenario Outline: Naming Standard on all available resources
    Given I have <resource_name> defined
    When it contains <name_key>
    Then its value must match the "myproject-(prod|uat|dev)-someapplication-.*" regex

    Examples:
    | resource_name           | name_key |
    | AWS EC2 instance        | name     |
    | AWS ELB resource        | name     |
    | AWS RDS instance        | name     |
    | AWS S3 Bucket           | bucket   |
    | AWS EBS volume          | name     |
    | AWS Auto-Scaling Group  | name     |
    | aws_key_pair            | key_name |
    | aws_ecs_cluster         | name     |
```

This is just an example where we assumed we have a naming standard that we apply 

* Project name (`myproject` in this example)
* Environment (`prod`, `uat` or `dev` in this example)
* Application Name (`someapplication` in this example)

to all resources that we create. The scenario above covers some of the resources that we want to check against.
