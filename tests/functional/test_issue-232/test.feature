Feature: test

  Scenario: Application load balancer must be internal
    Given I have aws_lb defined
    Then its internal must be true