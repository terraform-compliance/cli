Feature: Encryption with KMS

Scenario: Encryption via customer managed keys are present on all resources which take kms_key_id
  Given I have resource that supports kms_key_id defined
  Then it must contain kms_key_id
