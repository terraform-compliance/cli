Feature: Every reference inside a nested block is mounted

  Scenario: Lambda functions in a VPC use a managed security group
    Given I have aws_lambda_function defined
    Then it must have "aws_security_group.lambda" referenced

  Scenario: Lambda functions in a VPC use a managed subnet
    Given I have aws_lambda_function defined
    Then it must have "aws_subnet.private" referenced
