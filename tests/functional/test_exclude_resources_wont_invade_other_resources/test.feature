Feature: Test exclude resources 2
	excludion tag shouldn't interfere with any other scenarios

	Scenario: Data must be encrypted at rest
		Given I have aws_s3_bucket defined
		Then it must have server_side_encryption_configuration

	
	@exclude_aws_s3_bucket.mybucket2
	Scenario: Data stored in S3 has versioning enabled
		Given I have aws_s3_bucket defined
		Then it must have versioning
		Then it must have enabled
		And its value must be true
