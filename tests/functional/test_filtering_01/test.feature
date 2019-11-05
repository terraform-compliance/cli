Feature: Overpermissive Assume Role enforcement
  This feature checks if any assume role definition is overpermissive
  to enable rogue accounts to assume a role within our accounts.

  Scenario: Reject if a policy can assume ANY role in ANY account
    Given I have aws_iam_policy defined
    When it contains policy
    And it contains Statement
    And its Effect is Allow
    And its Action is sts:AssumeRole
    And it contains resource
    Then its value must not match the "\*" regex

  Scenario: Reject if the role can be assumed by ANY role in ANY account
    Given I have aws_iam_role defined
    When it contains assume_role_policy
    And it contains Statement
    And its Effect is Allow
    And its Action is sts:AssumeRole
    And it contains Principal
    And it contains AWS
    Then its value must not match the "\*" regex
