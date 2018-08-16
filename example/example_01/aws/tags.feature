Feature: Resources should be properly tagged
  In order to keep track of resource ownership
  As engineers
  We'll enforce tagging on all resources

  Scenario Outline: Name tag
    Given I have resource that supports tags defined
    Then it must contain tags
    And it must contain <tags>

  Examples:
  | tags        |
  | Name        |
  | application |
  | role        |
  | environment |