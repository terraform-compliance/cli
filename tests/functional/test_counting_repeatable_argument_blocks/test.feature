Feature: Count bug

  Scenario: Ensure one network is attached to one
    Given I have aws_instance defined
    When its name is one
    And it contains network_interface
    And I count them
    Then I expect the result is equal to 1

  Scenario: Ensure two networks are attached to two
    Given I have aws_instance defined
    When its name is two
    And it contains network_interface
    And I count them
    Then I expect the result is equal to 2