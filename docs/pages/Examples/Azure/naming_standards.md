---
layout: default
title: Naming Standards
nav_order: 1
has_children: false
parent: AWS
---

AWS
{: .label .label-yellow } 

* Table of Contents
{:toc}

# Examples about Naming Standards
## Naming Standard on all available resources
```gherkin
  Scenario Outline: Naming Standard on all available resources
    Given I have <resource_name> defined
    When it has <name_key>
    Then it must have <name_key>
    Then its value must match the "myproject-(prod|uat|dev)-someapplication-.*" regex

    Examples:
    | resource_name                          | name_key |
    | azurerm_network_interface              | name     |
    | azurerm_windows_virtual_machine        | name     |

  

```

This is just an example where we assumed we have a naming standard that we apply 

* Project name (`myproject` in this example)
* Environment (`prod`, `uat` or `dev` in this example)
* Application Name (`someapplication` in this example)

to all resources that we create. The scenario above covers some of the resources that we want to check against.
