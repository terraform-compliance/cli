Feature: feature for issue #310

	@noskip_at_line_6
	Scenario: solution without specific names
		Given I have aws_lambda_function defined
		Given I have aws_cloudwatch_log_group defined
		Then it must have name
		And it must cover /aws/lambda/{aws_lambda_function.values.function_name}

