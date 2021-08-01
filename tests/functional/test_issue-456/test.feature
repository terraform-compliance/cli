Feature: Feature for issue 456

	Scenario: Check if source is correctly being pulled
		Given I have aws_ecr_repository defined
		When its source metadata is ./modules/ecr_module
		When I count them
		Then its value must be equal to 5

	Scenario: Check that modules within the same directory doesn't bleed into other modules
		Given I have aws_ecr_repository defined
		When its source metadata is ./modules/other_ecr_module
		When I count them
		Then its value must be equal to 8

	Scenario: Check if non_module resources are affected (1)
		Given I have aws_ecr_repository defined
		When its name is non_module_bar
		When its source metadata is ./modules/ecr_module
		Then it must fail

	Scenario: Check if non_module resources are affected (2)
		Given I have aws_ecr_repository defined
		When its name is non_module_bar
		When its source metadata is ./modules/other_ecr_module
		Then it must fail

	# not writing a test for having source = ''
	# It's a safe undefined behavior
	# Ideally, non-module resources shouldn't have the source field at all, which is the case at the moment I'm writing this