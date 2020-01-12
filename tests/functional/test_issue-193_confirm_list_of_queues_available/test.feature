Feature: Test Scenario

  Scenario Outline: App Error queue exists
    Given I have azurerm_servicebus_queue defined
    When it contains name
    Then its value must not contain <name>

    Examples:

      | name                |
      | notexisting         |
    