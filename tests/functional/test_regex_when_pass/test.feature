Feature: Testing regex when
	plan has two grants:
		- full control
		- read, write
	
	test 1 (testing any - passes)
		One resource should remain in stash, since the permission includes something that doesn't match the stash

	test 2 (testing regular - passes)
		All values do not match the regex on one of the permissions

	test 3 (testing regular - passes)
		All values do match the regex so all values passes


	Scenario: test 1
		Given I have aws_s3_bucket defined
		When it has grant
		Then it must contain permissions
		When any of its values doesn't match the "(^WRITE$)|(^WRITE_ACP$)|(^FULL_CONTROL$)" regex

	Scenario: test 2
		Given I have aws_s3_bucket defined
		When it has grant
		Then it must contain permissions
		When its value doesn't match the "(^WRITE_ACP$)|(^FULL_CONTROL$)" regex

	Scenario: test 3
		Given I have aws_s3_bucket defined
		When it has grant
		Then it must contain permissions
		When its value matches the "(^WRITE$)|(^READ$)|(^FULL_CONTROL$)" regex

