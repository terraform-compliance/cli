Feature: Security Groups related general feature

	Scenario: No security group rule allow ingress from 0.0.0.0:0 to port 22
		Given I have aws_security_group_rule defined
		When its type is ingress
		And its to_port is 22
		Then it must contain cidr_blocks
		And it must not contain 0.0.0.0/0
