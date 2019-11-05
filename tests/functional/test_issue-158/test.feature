Feature: AWS
  This feature makes sure we configure aws providers appropriately.

  Scenario: Ensure we set allowed_account_ids
    Given I have aws provider configured
    Then it must contain allowed_account_ids