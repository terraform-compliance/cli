---
layout: default
title: BDD Reference
nav_order: 4
has_children: true
---

# BDD Reference

`terraform-compliance` utilises [radish](http://radish-bdd.io/) to handle BDD directives. BDD is
used in many development practices from End-to-End testing to FrontEnd testing, provides easy-to-understand
context that is self-descriptive and easy-to-understand for someone that is reading the test results.

In BDD, every feature file will have 3 components ;
        
- Feature
- Scenario/Scenario Outline
- Steps

### Feature
This draws the overall picture of the feature file that may consist several scenarios.

For e.g. ;

```gherkin
Feature: Security Groups should be used to protect services/instances
  In order to improve security
  As engineers
  We'll use AWS Security Groups as a Perimeter Defence
```

This won't effect anything about the test steps, but it will ease the pain for everybody to 
understand what does that feature aims for.

### Scenario
Every feature might have multiple scenarios. A scenario will define a test that might include multiple steps with BDD directives like ;

- GIVEN
- WHEN
- THEN

and every step might also have an additional extension step starting with ;
- AND

There are two types of Scenario ;

- Scenario : Used for defining a scenario without any multiple dynamic variables.
- Scenario Outline : Used for defining a scenario loops by giving multiple dynamic variables.

A Scenario can be like ;

```gherkin
Scenario: Ensure all resources have tags
    Given I have resource that supports tags defined
    Then it must contain tags
    And its value must not be null
```

Where a Scenario Outline could be ;

```gherkin
Scenario Outline: Ensure that specific tags are defined
    Given I have resource that supports tags defined
    When it contains tags
    Then it must contain <tags>
    And its value must not be null
    
    Examples:
      | tags           |
      | Name           |
      | Business Unit  |
      | Cost Centre    |
      | Environment    |
      | Major Function |
      | Service        |
      | Work Order     |
      | Service Level  |
      | Creator        |
```

### Steps
Steps are the functional tests that is actually executing necessary task to validate if the test is successful or not.

`terraform-compliance` has fixed steps already defined within the tool. It is possible to drill down your terraform resources by using these fixed steps.

