Feature: Test Scenario

  Scenario: Test Scenario - Success
    Given I have aws_s3_bucket defined
    When it has website
    Then its acl must be private

  Scenario: Test Scenario - Success #2
    Given I have aws_s3_bucket defined
    When it does not have website
    Then its acl must be public

  Scenario: Test Scenario - Failure #1
    Given I have aws_s3_bucket defined
    When it does not have website
    Then its acl must be private

  Scenario: Test Scenario - Skip #1
    Given I have aws_s3_bucket defined
    When it does not have acl
    Then its acl must be private