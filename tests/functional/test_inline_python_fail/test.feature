Feature: Test inline python fail
	
	Scenario: using inline python
		Given I have aws_vpc_peering_connection defined
		Then python "file1.py" "test_function"
