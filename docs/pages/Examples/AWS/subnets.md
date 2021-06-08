---
layout: default
title: Subnets
nav_order: 9
has_children: false
parent: AWS
---

AWS
{: .label .label-yellow } 

* Table of Contents
{:toc}

# Examples about Subnets
## Ensure a multi-layered network architecture
```gherkin
  Scenario: Ensure a multi-layered network architecture
    Given I have AWS Subnet defined
    When I count them
    Then I expect the result is more than 2
```
