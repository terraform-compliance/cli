Feature: test

      Scenario: SNS topics must be encrypted with kms
        Given I have aws_sns_topic defined
        Then it must contain kms_master_key_id
        And its value must not be null