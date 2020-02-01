Feature: Security Groups should be used to protect services/instances (Standard)
  In order to improve security
  As engineers
  We'll use Security Groups as a Perimeter Defence

  Scenario Outline: Avoid Well-known insecure protocol exposure on Public Network for ingress traffic (AWS Standard)
    Given I have AWS Security Group defined
    When it contains ingress
    Then it must not have <proto> protocol and port <portNumber> for 0.0.0.0/0


    Examples:
      | ProtocolName | proto | portNumber |
      | Telnet       | tcp   | 23         |
