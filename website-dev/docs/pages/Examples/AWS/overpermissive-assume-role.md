---
layout: default
title: Overpermissive Roles
nav_order: 5
has_children: false
parent: AWS
---

AWS
{: .label .label-yellow } 

* Table of Contents
{:toc}

# Examples about IAM AssumeRole

## Reject if a policy can assume ANY role in ANY account
```gherkin
Scenario: Reject if a policy can assume ANY role in ANY account
    Given I have aws_iam_policy defined
    When it contains policy
    And it contains Statement
    And its Effect is Allow
    And its Action is sts:AssumeRole
    And it contains resource
    Then its value must not match the "\*" regex
```

## Reject if the role can be assumed by ANY role in ANY account
```gherkin
Scenario: Reject if the role can be assumed by ANY role in ANY account
    Given I have aws_iam_role defined
    When it contains assume_role_policy
    And it contains Statement
    And its Effect is Allow
    And its Action is sts:AssumeRole
    And it contains Principal
    And it contains AWS
    Then its value must not match the "\*" regex
```

## Reject if the role can be assumed by ANY account other than specific AWS accounts
```gherkin
   Scenario: Reject if the role can be assumed by ANY account other than specific AWS accounts
        Given I have aws_iam_role defined
        When it contains assume_role_policy
        And it contains Statement
        And its Effect is Allow
        And its Action is sts:AssumeRole
        And it contains Principal
        And it contains AWS
        Then its value must match the ".*1234567890*|.*1234567891*" regex
```