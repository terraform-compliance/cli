Feature: Test Scenario

  Scenario Outline: App Error queue exists
    Given I have azurerm_servicebus_queue defined
    When its index is <name>
    Then it must contain enable_partitioning
    And its value must be <partitioning>

    Examples:

    | name                | partitioning |
    | something           | true         |
    | somethingelse       | true         |
    | somethingdifferent  | false        |