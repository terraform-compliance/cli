Feature: Data example feature

  Scenario: Subnet Count
    Given I have aws_availability_zones data defined
    When it contains zone_ids
    And I count them
    Then I expect the result is greater than 2

  Scenario: Subnet Count
    Given I have aws_availability_zones data defined
    When it contains zone_ids
    And I count them
    Then I expect the result is equal to 3
