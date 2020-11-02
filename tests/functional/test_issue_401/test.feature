Feature: Feature for testing its_key_is_value

	Scenario: Ensure all data stored in the RDS is securely encrypted at rest
		Given I have aws_db_instance defined
		When its replicate_source_db is None
		Then it must have storage_encrypted
		And its value must be true


	Scenario: Ensure all data stored in the RDS is securely encrypted at rest (not)
		Given I have aws_db_instance defined
		When its replicate_source_db is not notNone
		Then it must fail