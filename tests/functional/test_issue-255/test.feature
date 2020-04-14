Feature: Terraform-BDD
  Scenario: Ensure s3 buckets deployed privately
    Given I have aws_s3_bucket_policy defined
    When it contains policy
    And it contains Statement
    And its Effect is Allow
    And its Action contains s3:*
    And it contains resource
    Then its value must not match the "\*" regex
