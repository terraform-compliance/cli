Feature: Feature for issue 424
	
	Scenario: Dummy scenario
		Given I have aws_ecr_repository defined
		Then it must have image_scanning_configuration
		Given I have aws_iam_role defined
		Then it must have Statement
		