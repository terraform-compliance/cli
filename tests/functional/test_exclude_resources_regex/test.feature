Feature: Feature for issue 424
	
	@exclude_module.ecr_repository\[\"repository_2\"\].aws_ecr_repository.ecr_repository
	@exclude_module.ecr_repository\[\"repository_1\"\].aws_ecr_repository.ecr_repository
	Scenario: Dummy scenario
		Given I have aws_ecr_repository defined
		Then it must fail

	@exclude_module.ecr_repository\[\"repository_[0-9]\"\].aws_ecr_repository.ecr_repository
	Scenario: Dummy 2
		Given I have aws_ecr_repository defined
		Then it must fail
		
	@exclude_module.ecr_repository.*aws_ecr_repository.ecr_repository
	Scenario: Dummy 3
		Given I have aws_ecr_repository defined
		Then it must fail
