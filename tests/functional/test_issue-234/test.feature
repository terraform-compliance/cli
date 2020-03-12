Feature: test

  Scenario Outline: Application load balancer security group allows load balancer to communicate with itself
    Given I have aws_security_group_rule defined
    When its security_group_id reference is aws_security_group.alb
    And its type is <type>
    Then its protocol must be tcp
    And its from_port must be 0
    And its to_port must be 65535
    And it must contain self
    And its value must be <test>

    Examples:
    | type      | test |
    | ingress   | true |
    | egress    | true |
