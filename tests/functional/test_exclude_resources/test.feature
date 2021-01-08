Feature: Test exclude resources
	
	mybucket2 would fail if not excluded

	@exclude_aws_s3_bucket.mybucket2
	Scenario: Data stored in S3 has versioning enabled
		Given I have aws_s3_bucket defined
		Then it must have versioning
		Then it must have enabled
		And its value must be true

	@ignore_aws_s3_bucket.mybucket2
	Scenario: Data stored in S3 has versioning enabled (ignore)
		Given I have aws_s3_bucket defined
		Then it must have versioning
		Then it must have enabled
		And its value must be true
