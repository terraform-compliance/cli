Feature: Virtual machines must use approved configurations
  In order to keep consistency between resources
  As engineers
  We'll enforce the virtual machine configurations

  Scenario Outline: Ensure that VM specific tags are defined
    Given I have azurerm_virtual_machine defined
    When it has tags
    Then it must contain tags
    Then it must contain <tag>
    And its value must match the "<value>" regex

    Examples:
      | tag         | value                        |
      | backmeup    | (true\|false)                |
      | terraform   | (true)                       |