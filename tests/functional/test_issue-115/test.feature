Feature: Test for https://github.com/eerkunt/terraform-compliance/issues/115

  Scenario: Ensure IAM Actions does not have everything in it
    Given I have aws_iam_policy defined
    Then it must contain policy
    And it must contain Statement
    And it must contain Action
    And Then its value must match the "^(kms:Encrypt|kms:Decrypt)$" regex
