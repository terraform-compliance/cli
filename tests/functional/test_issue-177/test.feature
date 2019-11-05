Feature: test

  Scenario: Reject if a policy can assume ANY role in ANY account
    Given I have aws_iam_policy defined
    When it contains policy
    And it contains Statement
    And its Effect is Allow
    And its Action is sts:AssumeRole
    And it contains resource
    Then its value must not match the "\*" regex