Feature: Plans that forward a nested module output must be parsed

  Scenario: null_resource triggers are mounted
    Given I have null_resource defined
    Then it must contain triggers
