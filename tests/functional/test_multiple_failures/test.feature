Feature: Test feature

  Scenario: Multiple failures test on port 80
    Given I have AWS Security Group defined
    When it contains ingress
    Then it must not have tcp protocol and port 80 for 0.0.0.0/0
