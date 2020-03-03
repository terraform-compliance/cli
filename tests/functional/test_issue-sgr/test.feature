Feature: test

  Scenario: No 0.0.0.0/0 for ingress on rule
    Given I have aws_security_group_rule defined
    When its type is ingress
    Then its from_port must be 0
