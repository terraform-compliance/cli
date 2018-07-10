Feature: Security Groups should be used to protect services/instances
  In order to improve security
  As engineers
  We'll use AWS Security Groups as a Perimeter Defence

  Scenario Outline: Policy Structure
    When I define AWS Security Group
    Then it must contain <policy_name>

  Examples:
    | policy_name |
    | ingress     |
    | egress      |

  Scenario Outline: Well-known insecure protocol exposure on Public Network for ingress traffic
  	When I define AWS Security Group
  	Then it must contain ingress
  	with <proto> protocol and not port <portNumber> for 0.0.0.0/0

  Examples:
    | ProtocolName | proto | portNumber |
    | HTTP         | tcp   | 80         |
    | Telnet       | tcp   | 23         |
    | SSH          | tcp   | 22         |
    | MySQL        | tcp   | 3306       |
    | MSSQL        | tcp   | 1443       |
    | NetBIOS      | tcp   | 139        |
    | RDP          | tcp   | 3389       |
