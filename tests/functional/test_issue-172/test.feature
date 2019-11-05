Feature: test

  Scenario: Enforce the listener ports
    Given I have aws_lb_listener resource configured
    When its protocol is TCP
    Then it must contain port
    And its value must be 443