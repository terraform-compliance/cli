Feature: feature for issue #562
	Passing tests for all it_must_not_be_in variations
	lambdas and cloudwatch groups match
	Did not repeat noskip, as it was unnecessary

	@noskip_at_line_6
	Scenario: must not cover
		Given I have aws_cloudwatch_log_group defined
		Given I have aws_lambda_function defined
		Then it must have function_name
		And it must not cover {aws_cloudwatch_log_group.values.name}


	Scenario: must not be a superset of
		Given I have aws_cloudwatch_log_group defined
		Given I have aws_lambda_function defined
		Then it must have function_name
		And it must not be a superset of {aws_cloudwatch_log_group.values.name}
