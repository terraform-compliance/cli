---
layout: default
title: Noskip Examples
nav_order: 2
has_children: false
parent: Azure
---
# Noskip Examples

Noskip tag fails the scenario or step if it skips. Using this tag lets us use `GIVEN` and `WHEN` steps similar to a `THEN` step.

## Reference
* Table of Contents
{:toc}

## Then I must have resource defined
Since `THEN` steps exclusively drill down the resource passed from the previous step, we could not write the `THEN` step below, which checks the existence of something outside of its context.

```
Given I have azurerm_postgresql_server defined
Then I must have azurerm_postgresql_configuration defined
```

With `@noskip`, we can:
```
@noskip_at_line_3
Scenario: resource A implies resource B
    Given I have azurerm_postgresql_server defined
    Given I have azurerm_postgresql_configuration defined # line 3
```
Note that the scenario doesn't fail if azurerm_postgresql_server doesn't exist. It only fails when there is the first resource but not the second.


## Filtering Then
Since `THEN` steps exlusively drill down, we can't write consecutive `THEN` steps that check the properties of the same resource within that resource and stay on the same level. 

we would need to write a new scenario if we wanted to check a property that was lost during the "drill"

```
resource "azurerm_postgresql_configuration" "log_checkpoints" {
  name                = "log_checkpoints"
  resource_group_name = azurerm_resource_group.example.name
  server_name         = azurerm_postgresql_server.example.name
  value               = "on"
}

resource "azurerm_postgresql_configuration" "log_connections" {
  name                = "log_connections"
  resource_group_name = azurerm_resource_group.example.name
  server_name         = azurerm_postgresql_server.example.name
  value               = "on"
}

... # many more configurations
```

If I wanted to accomplish
```
If I have azurerm_postgresql_server
    - server parameter 'log_checkpoints' must be set to 'ON' for PostgreSQL Database Server
```
Using `THEN its name bust be log_connections` would drill down to `log_connections` and we wouldn't be able check if the value is on or not.

With `@noskip`, we can:
```
@noskip_at_lines_4_5
Scenario Outline: Filtering then
    Given I have azurerm_postgresql_server defined
    Given I have azurerm_postgresql_configuration defined  # line 4
    When its name is log_checkpoints  # line 5
    Then it must have value
    Then its value must match the "on" regex

```

Note that on line 5, we don't drill down to name but still fail if there is no "log_checkpoints"

## Using noskip with scenario outlines

```
# main.tf

resource "azurerm_postgresql_configuration" "log_checkpoints" {
  name                = "log_checkpoints"
  resource_group_name = azurerm_resource_group.example.name
  server_name         = azurerm_postgresql_server.example.name
  value               = "on"
}

resource "azurerm_postgresql_configuration" "connection_throttling" {
  name                = "connection_throttling"
  resource_group_name = azurerm_resource_group.example.name
  server_name         = azurerm_postgresql_server.example.name
  value               = "off"
}

resource "azurerm_postgresql_configuration" "log_retention_days" {
  name                = "log_retention_days"
  resource_group_name = azurerm_resource_group.example.name
  server_name         = azurerm_postgresql_server.example.name
  value               = "4"
}

# ... (many more azurerm_postgresql_configurations below)
```


```gherkin
@noskip_at_lines_22_23_24
Scenario Outline: Scenario for issue #291
    Given I have azurerm_postgresql_configuration defined
    When its name is <config_name>
    Then it must have value
    Then its value must match the "<value>" regex

    Examples:
    | config_name           | value            |
    | log_checkpoints       | on               | # line 22
    | connection_throttling | off              | # line 23
    | log_retention_days    | ^([4-9]\|\d{2,})$| # line 24
    # ...
```

Which is equivalent to only using `@noskip`
