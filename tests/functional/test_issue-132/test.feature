Feature: https://github.com/eerkunt/terraform-compliance/issues/132

  Scenario: This scenario must fail #1
    Given I have aws_sagemaker_notebook_instance defined
    Then it must contain kms_key_id
    And its value must match the ".*kms.*" regex

  Scenario: This scenario must fail #2
    Given I have aws_sagemaker_notebook_instance defined
    Then it must contain kms_key_id
    And its value must not be null