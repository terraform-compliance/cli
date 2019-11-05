Feature: Resources should be properly tagged  # /target/tc-test2/features/tags.feature
  In order to keep track of resource ownership
  As engineers
  We'll enforce tagging on all resources

#  Scenario Outline: Ensure that my specific tags are defined
#    Given I have resource that supports tags defined
#    When it contains tags
#    Then it must contain <tag_keys>
#    And its value must match the "<pattern>" regex
#
#    Examples:
#      | tag_keys            | pattern                                                                  |
#      | application         | ^([a-z]+[0-9]*)*[-]?([a-z0-9]+[-])*[a-z0-9]+$                            |
#      | app_component       | ^([a-z]+[0-9]*)*[-]?([a-z0-9]+[-])*[a-z0-9]+$                            |
#      | app_contacts        | ^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$                          |
#      | app_environment     | ^(sandbox\|dev\|deva\|devb\|ita\|itb\|qa\|pv\|prod\|poc\|training)$      |
#
#
#  Scenario Outline: Policy Structure
#    Given I have AWS Security Group defined
#    Then it must contain <policy_name>
#
#    Examples:
#      | policy_name |
#      | ingress     |
#
#  Scenario Outline: Well-known insecure protocol exposure on Public Network for ingress traffic
#    Given I have AWS Security Group defined
#    When it contains ingress
#    Then it must not have <proto> protocol and port <portNumber> for 10.0.0.0/8
#
#    Examples:
#      | ProtocolName  | proto | portNumber |
#      | HTTP          | tcp   | 443        |
#      | Telnet        | tcp   | 23         |
#      | SSH           | tcp   | 22         |
#      | MySQL         | tcp   | 3306       |
#      | MSSQL         | tcp   | 1443       |
#      | NetBIOS       | tcp   | 139        |
#      | RDP           | tcp   | 3389       |
#      | Jenkins Slave | tcp   | 50000      |

  Scenario: Ensure we only allow a port range for ingress rule
    Given I have AWS Security Group defined
    When it contains ingress
    Then it must only have tcp protocol and port 22 for 10.0.0.0/8
