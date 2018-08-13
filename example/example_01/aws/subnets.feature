Feature: Subnets should be defined properly for network security
  In order to improve security
  And decrease impact radius
  As engineers
  We'll use a layered architecture in our AWS Environment

  Scenario: Subnet Count
    Given I have AWS Subnet defined
    When I count them
    Then I expect the result is more than 2
