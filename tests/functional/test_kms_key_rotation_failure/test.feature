Feature: KMS Key rotation enforcement
    This feature checks if any custom KMS Key is created without rotation.

    Scenario: Reject if a custom KMS key is created without key rotation
        Given I have aws_kms_key defined
        Then it must contain enable_key_rotation
        And its value must be true
