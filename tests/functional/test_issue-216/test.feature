Feature: Security group(s) attached to ECS task must restrict inbound and outbound traffic

#    Scenario Outline: ECS security group allows communication with itself
#        Given I have aws_security_group_rule defined
#        When its security_group_id reference is "aws_security_group.ecs_task"
#        And its self is true
#        Then its protocol must be tcp
#        And its from_port must be 0
#        And its to_port must be 65535
#        And its type must be <type>
#
#        Examples:
#            | type    |
#            | ingress |
#            | egress  |
#
#    Scenario: ECS task security group allows egress to Internet on port 443
#        Given I have aws_security_group_rule defined
#        When its security_group_id reference is "aws_security_group.ecs_task"
#        And its from_port is 443
#        Then its protocol must be tcp
#        And its to_port must be 443
#        And it must contain cidr_blocks
#        And its value must contain 0.0.0.0/0

    Scenario: ECS task security group allows egress to Internet on port 443 with shorter steps
        Given I have aws_security_group_rule defined
        When its security_group_id reference is "aws_security_group.ecs_task"
        And its type is egress
        And its from_port is 443
        Then it must have tcp protocol and port 443 for 192.*
