Feature: Correctly defined tags on all applicable resources
  I need to ensure all resources that support tags have a bare minimal set in place

  Scenario Outline: Ensure we have specific tags in place
    Given I have resource that supports tags defined
    Then it must contain <tags>
    And its value must match the "<value>" regex

    Examples:
      | tags        | value        |
      | Name        | ^mcrilly-.+$ |
      | Environment | ^Sandbox$    |
