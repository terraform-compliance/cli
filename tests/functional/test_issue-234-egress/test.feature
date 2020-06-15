Feature: test egress

    Background: Application load balancer security group allows load balancer to communicate with itself
        Given I have aws_security_group_rule defined
        When its security_group_id reference is aws_security_group.alb
        And its type is egress

    Scenario: something 0
        Then its protocol must be tcp

  
    Scenario: something 1
        Then its from_port must be 0

    Scenario: something 2
        Then its to_port must be 65535

    Scenario: something 3
        Then it must contain self
        Then its value must be true


  