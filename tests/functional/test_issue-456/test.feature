Feature: Feature for issue 456

	Scenario: Check if source is correctly being pulled
		Given I have aws_ecr_repository defined
		When its source metadata is ./modules/ecr_module
		When I count them
		Then its value must be equal to 2


	Scenario: Check that modules within the same directory doesn't bleed into other modules
		Given I have aws_ecr_repository defined
		When its source metadata is ./modules/other_ecr_module
		When I count them
		Then its value must be equal to 1		