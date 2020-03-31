Feature: test

  Scenario: Ensure I have all groups
    Given I have gsuite_group defined
    When it contains email
    And I count them
    Then its value must be equal to 2
