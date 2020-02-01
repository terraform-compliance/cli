Feature: https://github.com/eerkunt/terraform-compliance/issues/157#issuecomment-563133956

  Scenario: Fail if resource_b has not been defined
    Given I have aws_s3_bucket defined
    Then the scenario should fail
