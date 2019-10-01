---
layout: default
title: KMS
nav_order: 1
has_children: false
parent: Examples
---

AWS
{: .label .label-yellow } 

* Table of Contents
{:toc}

# Examples about KMS
## Reject if a custom KMS key is created without key rotation
```gherkin
    Scenario: Reject if a custom KMS key is created without key rotation
        Given I have aws_kms_key defined
        Then it must contain enable_key_rotation
        And its value must be true
```

## Reject if a custom KMS key is created with over permissive policy with * value
```gherkin
Scenario: Reject if a custom KMS key is created with over permissive policy with * value
        Given I have aws_kms_key defined
        When it contains policy
        And it contains Statement
        And its Effect is Allow 
        And it contains Principal
        Then its value must not match the "\*" regex
```

## Reject if a custom KMS key is created with over permissive policy which allows access to accounts other than specific accounts
```gherkin
Scenario: Reject if a custom KMS key is created with over permissive policy which allows access to accounts other than specific accounts
        Given I have aws_kms_key defined
        When it contains policy
        And it contains Statement
        And its Effect is Allow 
        And it contains Principal
        Then its value must match the ".*123456789012|.*.amazonaws.com" regex
```
