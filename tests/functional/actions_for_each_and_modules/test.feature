Feature: Feature for issue 408, adding Terraform's actions to the resource
	modules and for_each
	
	Scenario: create on aws_ecr_repository
		Given I have aws_ecr_repository defined
		When its actions metadata does not have create
		Then it must fail

	Scenario: create on aws_iam_role
		Given I have aws_iam_role defined
		When its actions metadata does not have create
		Then it must fail
		