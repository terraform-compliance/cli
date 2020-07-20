Feature: hi

	Scenario: No 0.0.0.0/0 for ingress on rule
        Given I have aws_security_group_rule defined
        When its type is ingress
        And it has cidr_blocks