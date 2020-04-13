Feature: test

  Scenario: IAM prefix must be reference by all IAM resources
    Given I have aws_iam_role defined
    Then it must have "module.test.random_id.iam_prefix" referenced
