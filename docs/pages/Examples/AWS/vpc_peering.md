---
layout: default
title: VPC Peering
nav_order: 11
has_children: false
parent: Examples
---

AWS
{: .label .label-yellow } 

* Table of Contents
{:toc}

# Examples about VPC Peering
## Owner and Peer Validation
```gherkin
Scenario Outline: Owner and Peer Validation
    Given I have aws_vpc_peering_connection defined
    When it has <key>
    Then it must have <key>
    Then its value must match the "<value>" regex

  Examples:
  | key           | value        |
  | peer_owner_id | 123456789    |
  | peer_vpc_id   | vpc-1a2b3c4d |
```
