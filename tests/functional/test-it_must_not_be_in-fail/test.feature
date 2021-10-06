Feature: feature for issue #562
	Passing tests for all it_must_not_be_in variations
	1:1 between lambdas and cloudwatch groups
	Did not repeat noskip, as it was unnecessary

	@noskip_at_line_6
	Scenario: must not be in
		Given I have aws_cloudwatch_log_group defined
		Given I have aws_lambda_function defined
		Then it must have function_name
		And it must not be in {aws_cloudwatch_log_group.values.name}


	Scenario: must not be a subset of
		Given I have aws_cloudwatch_log_group defined
		Given I have aws_lambda_function defined
		Then it must have function_name
		And it must not be a subset of {aws_cloudwatch_log_group.values.name}

