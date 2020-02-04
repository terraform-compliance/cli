Feature: Issue 203, must pass

  Scenario: Reject if the role can be assumed by ANY role in ANY account
    Given I have aws_iam_role defined
    When it contains assume_role_policy
    And it contains Statement
    And its Effect is Allow
    And its Action is sts:AssumeRole
    And it contains Principal
    And it contains AWS
    Then its value must not match the "\*" regex