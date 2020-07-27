Feature: feature for issue #310
	Passing tests for all it_must_be_in variations
	1:1 between lambdas and cloudwatch groups
	Did not repeat noskip, as it was unnecessary

	@noskip_at_line_6
	Scenario: must be in
		Given I have aws_cloudwatch_log_group defined
		Given I have aws_lambda_function defined
		Then it must have function_name
		And it must be in {aws_cloudwatch_log_group.values.name}


	Scenario: must be a subset of
		Given I have aws_cloudwatch_log_group defined
		Given I have aws_lambda_function defined
		Then it must have function_name
		And it must be a subset of {aws_cloudwatch_log_group.values.name}


	Scenario: must cover
		Given I have aws_cloudwatch_log_group defined
		Given I have aws_lambda_function defined
		Then it must have function_name
		And it must cover {aws_cloudwatch_log_group.values.name}


	Scenario: must be a superset of
		Given I have aws_cloudwatch_log_group defined
		Given I have aws_lambda_function defined
		Then it must have function_name
		And it must be a superset of {aws_cloudwatch_log_group.values.name}
