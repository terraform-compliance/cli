---
layout: default
title: Encryption
nav_order: 2
has_children: false
parent: AWS
---

AWS
{: .label .label-yellow } 

* Table of Contents
{:toc}

# Encryption-in-flight
## TLS Enforcement on ELB resources
```gherkin
  Scenario: TLS enforcement on ELB resources
    Given I have AWS ELB resource defined
    When it contains listener
    Then it must contain ssl_certificate_id
```

## Enforce encryption for EMR
```gherkin
  Scenario: Enforce encryption for EMR
    Given I have AWS EMR Security Configuration defined
    Then encryption in flight must be enabled
```

## Enforce encryption in ElastiCache Replication
```gherkin
  Scenario: Enforce encryption in ElastiCache Replication
    Given I have AWS ElastiCache Replication Group defined
    Then encryption in flight must be enabled
```

