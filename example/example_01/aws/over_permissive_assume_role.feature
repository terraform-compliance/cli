Feature: Overpermissive Assume Role enforcement
  This feature checks if any assume role definition is overpermissive
  to enable rogue accounts to assume a role within our accounts.

  Scenario: Reject if AWS Principal is for ALL accounts
    Given I have aws_iam_policy defined
    When it contains policy
    And it contains Statement
    And its Action is sts:AssumeRole
    And it contains resource
    Then its value must not match the "\*" regex
