Feature: test

  Scenario: Bucket policy must have at least one deny statement
    Given I have aws_s3_bucket_policy defined
    When it contains policy
    And it contains Statement
    And it contains Effect
    Then its value must be Deny
