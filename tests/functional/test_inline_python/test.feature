Feature: test inline python
	
	Scenario: dummy scenario to test importing multiple files
		Given I have aws_vpc_peering_connection defined
		Then Python file1.py dummy_function
		Then python "file2.py" "dummy_function"
		Then python "file2.py" "dummy_function"
		Then python "file1.py" "dummy_function"

	Scenario: Test if changes were applied on stash
		Given I have aws_vpc_peering_connection defined
		Then it must pass python test "file3.py" "test_function"
		Then it must have description
		And its value must be "I have complete control over my tests"
