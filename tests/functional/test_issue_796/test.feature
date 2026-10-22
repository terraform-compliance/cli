Feature: Lambda permissions must not be public

  Scenario: aws_lambda_permission must have source_arn
    Given I have aws_lambda_permission defined
    Then it must have source_arn
    Then its value must not be None
