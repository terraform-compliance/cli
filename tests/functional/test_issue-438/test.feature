Feature: Feature for issue 438

Scenario: Resource that supports should not skip
  Given I have resource that supports kms_key_id defined
  Then it must contain kms_key_id
  And its value must not be null
