Feature: test

  Scenario: Only allow TLS and TCP protocols on NLBs
    Given I have aws_lb_listener resource configured
    When it contain protocol
    Then its value must not match the ".*(UDP|udp)" regex
