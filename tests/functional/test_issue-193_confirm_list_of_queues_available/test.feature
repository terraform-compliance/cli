Feature: Test Scenario

  Scenario Outline: App Error queue exists
    Given I have azurerm_servicebus_queue defined
    Then it must contain name
    And I flatten all values found
    And its value must contain <name>

    Examples:

      | name                |
      | notexisting         |
      | something           |
      | somethingelse       |
      | somethingdifferent  |

  Scenario Outline: App Error queue have right partitioning
    Given I have azurerm_servicebus_queue defined
    When its index is <name>
    Then it must contain enable_partitioning
    And its value must be <partitioning>

    Examples:

      | name                | partitioning |
      | notexisting         | true         |
      | something           | true         |
      | somethingelse       | true         |
      | somethingdifferent  | false        |
