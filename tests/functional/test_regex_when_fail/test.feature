Feature: Testing regex when
	
	Note: skips are failed

	test 1 (testing regular - skips)
		Every permission contains one of the test listed so no resource should pass

	test 2 (testing regular - skips)
		For every permission, there's at least one value that doesn't match the regex

	test 3 (testing any - skips)
		For every permission, all values do not match the regex

	test 4 (testing any - skips)
		No permission has any value that matches the regex

	test 5 (testing error messages)
		If no resource in stash supports regex comparison, skip the step.

	@noskip	
	Scenario: test 1
		Given I have aws_s3_bucket defined
		When it has grant
		Then it must contain permissions
		When its value doesn't match the "(^WRITE$)|(^WRITE_ACP$)|(^FULL_CONTROL$)" regex

	@noskip	
	Scenario: test 2
		Given I have aws_s3_bucket defined
		When it has grant
		Then it must contain permissions
		When its value matches the "(^WRITE$)" regex

	@noskip
	Scenario: test 3
		Given I have aws_s3_bucket defined
		When it has grant
		Then it must contain permissions
		When any of its values doesn't match the "(^READ$)|(^WRITE$)|(^FULL_CONTROL$)" regex

	@noskip
	Scenario: test 4
		Given I have aws_s3_bucket defined
		When it has grant
		Then it must contain permissions
		When any of its values matches the "(^WRITE_ACP$)" regex

	@noskip
	Scenario: test 5
		Given I have aws_s3_bucket defined
		When it has grant
		Then it must have grant
		When any of its values does not match the "regex" regex