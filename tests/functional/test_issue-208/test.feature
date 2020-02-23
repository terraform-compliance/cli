Feature: test.feature

  Scenario Outline: All the things have tags
    Given I have resource that supports tags defined
    Then it must contain <tags>

    Examples:
      | tags        |
      | Capability  |
      | Environment |
