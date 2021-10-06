---
layout: default
title: Security Groups
nav_order: 8
has_children: false
parent: Examples
---

AWS
{: .label .label-yellow } 

* Table of Contents
{:toc}

# Examples about Security Groups

## Ensure our SG an Ingress policy
```gherkin
  Scenario Outline: Ensure our SG an Ingress policy
    Given I have AWS Security Group defined
    Then it must contain <policy_name>

  Examples:
    | policy_name |
    | ingress     |
```

## Well-known insecure protocol exposure on Public Network for ingress traffic

```gherkin
Scenario Outline: Well-known insecure protocol exposure on Public Network for ingress traffic
    Given I have AWS Security Group defined
    When it has ingress
    Then it must have ingress
    Then it must not have <proto> protocol and port <portNumber> for 0.0.0.0/0


  Examples:
    | ProtocolName | proto | portNumber |
    | HTTP         | tcp   | 443       |
    | Telnet       | tcp   | 23         |
    | SSH          | tcp   | 22         |
    | MySQL        | tcp   | 3306       |
    | MSSQL        | tcp   | 1443       |
    | NetBIOS      | tcp   | 139        |
    | RDP          | tcp   | 3389       |
    | Jenkins Slave| tcp   | 50000      |
```

## No publicly open ports

```gherkin
Scenario: No publicly open ports
    Given I have AWS Security Group defined
    When it has ingress
    Then it must have ingress
    Then it must not have tcp protocol and port 1024-65535 for 0.0.0.0/0
```

## Only selected ports should be publicly open

```gherkin
Scenario: Only selected ports should be publicly open
    Given I have AWS Security Group defined
    When it has ingress
    Then it must have ingress
    Then it must only have tcp protocol and port 22,443 for 0.0.0.0/0
```