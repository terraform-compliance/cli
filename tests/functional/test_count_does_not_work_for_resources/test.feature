Feature: test for https://github.com/eerkunt/terraform-compliance/issues/187

  Scenario: There is exactly one VPC
    Given I have any resource defined
    When its type is aws_vpc
    And I count them
    Then I expect the result is equal to 2
