Feature: Image scan to be enabled on push to ECR
  This feature will enforce vulnerabilty scan on images pushed to ECR
  ​
  Scenario: Image scan to be enabled on push.
    Given I have aws_dynamodb_table defined
    Then it must contain server_side_encryption
    And it must contain kms_key_arn
