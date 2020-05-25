Feature: test

  Scenario: This is for constant values
    Given I have aws_sqs_queue resource configured
    Then it must contain kms_master_key_id
    And its value must not be null