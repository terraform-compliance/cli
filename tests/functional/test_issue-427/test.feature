Feature: Feature for issue 427
	No steps needed, just make sure this plan can be parsed

    Scenario: VPC should be created
    	Given I have aws_route53_zone defined
    	Given I have aws_route53_record defined