Feature: S3 Restrictions for AWS Provider v4

  Scenario: AWS Provider v3
    Given I have aws provider configured
    When its version_constraint has "^3\..*" regex

  Scenario: AWS Provider v4
    Given I have aws provider configured
    When its version_constraint has "^4\..*" regex

  @precondition(test.feature: AWS Provider v4)
  Scenario: Ensure S3 bucket is Encrypted
    Given I have aws_s3_bucket defined
    Then it must have aws_s3_bucket_server_side_encryption_configuration

  @precondition(test.feature: AWS Provider v4)
  Scenario: Ensure S3 bucket has versioning configured
    Given I have aws_s3_bucket defined
    Then it must have aws_s3_bucket_versioning

  @precondition(test.feature: AWS Provider v4)
  Scenario: Ensure S3 bucket has logging configured
    Given I have aws_s3_bucket defined
    Then it must have aws_s3_bucket_logging

  @case-sensitive
  Scenario Outline: Ensure that specific tags are defined
    Given I have resource that supports tags defined
    When its address metadata is "module.project1.*" regex
    Then it must contain "<tags>"
    And its value must match the "<value>" regex

      Examples:
        | tags      | value   |
        | project   | project1 |