---
layout: default
title: Noskip Tag
nav_order: 1
has_children: false
parent: Using Tags
---

# Noksip Tag

In Terraform-Compliance, `WHEN` always filters and `THEN` always drills down. However, this might not what we want all the time. With `noskip`, conditions can be forced without having to drill down to their values.

Using `@noskip` fails the scenario if any of the steps skips. Using `@noskip_at_lines_2_3`, will fail if there are skipping steps within the scenario that falls into the lines 2 and 3

## Reference
* Table of Contents
{:toc}

# Examples

## Forcing a specific resource while the resources exists with the same type

Assume we wanted to specifically check `log_checkpoints` existed and is set to on, within a plan where there are many `azurerm_postgresql_configuration` resources.

```
# main.tf

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

# ... (many more azurerm_postgresql_configurations below)
```

To do so, we need to filter to the correct `azurerm_postgresql_configuration`, fail if it doesn't exist, then drill to its `value` to finally check whether it's on or not.

```
@noskip
Scenario: log checkpoints must exist and must be set to on. 
    Given I have azurerm_postgresql_configuration defined
    When its name is log_checkpoints
    Then it must have value
    Then its value must be on

```


If we used
```
    Given I have azurerm_postgresql_configuration defined
    When its name is not log_checkpoints
    Then it must fail
```
We wouldn't filter to the correct resources, since the `WHEN` step would capture all the configurations that are not `log_checkpoints`.


If we tried the following instead,
```
    Given I have azurerm_postgresql_configuration defined
    Then its name must be log_checkpoints
```
We would end up drilling to the `name`'s value `log_checkpoints`, which would prevent me from checking fields outside of this scope.

------------------------
## Resource A implies Resource B

`noskip` can be used for simulating implications between resources. 

Say we wanted the following to hold: if azurerm_postgresql_server is defined, then azurerm_postgresql_configuration must be defined.
The scenario should skip if there are no `azurerm_postgresql_server` defined but fail if it exists without any `azurerm_postgresql_configuration` defined.
```
@noskip_at_line_4
Scenario: Ensure azurerm_postgresql_configuration is defined if a PostgreSQL Database Server exists.
    Given I have azurerm_postgresql_server defined
    Given I have azurerm_postgresql_configuration defined   # line 4
```

Following also accomplishes the same.

```
@noskip_at_line_5
Scenario: Ensure azurerm_postgresql_configuration is defined if a PostgreSQL Database Server exists.
    Given I have azurerm_postgresql_server defined
    Given I have any resource defined
    When its type is azurerm_postgresql_configuration  # line 5
```

------------------------
## Using noskip with scenario outlines

Similar to [Forcing a specific resource while the resources exists with the same type](/pages/bdd-references/using_tags/using_noskip.html#forcing-a-specific-resource-while-the-resources-exists-with-the-same-type), we have a large list of `azurerm_postgresql_configuration`s. This time, we would like to check values of each configuration.

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


```
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
