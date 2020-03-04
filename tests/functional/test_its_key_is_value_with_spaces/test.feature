Feature: Allow spaces in value for its_key_is_value filter

  Scenario: A tag without spaces
    Given I have aws_s3_bucket defined
    When its tags includes WithoutSpace
    Then it must fail

  Scenario: A tag that includes spaces
    Given I have aws_s3_bucket defined
    When its tags includes "With Space"
    Then it must fail

  Scenario: A tag without spaces (negative)
    Given I have aws_s3_bucket defined
    When its tags does not include WithoutSpace
    Then it must fail

  Scenario: A tag that includes spaces (negative)
    Given I have aws_s3_bucket defined
    When its tags does not include "With Space"
    Then it must fail