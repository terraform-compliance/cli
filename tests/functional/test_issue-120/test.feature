Feature: Test for https://github.com/eerkunt/terraform-compliance/issues/120

  Scenario: Ensure backup retention period is defined
    Given I have aws_rds_cluster defined
    Then it must contain backup_retention_period
    And its value must be greater than 15
