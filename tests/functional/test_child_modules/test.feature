Feature: Feature for issue 494, adding support for Child Modules
	This features confirms if child modules is supported

	@noskip
  	Scenario: Check if an S3 bucket is encrypted
 		Given I have aws_s3_bucket defined
 		Then it must contain server_side_encryption_configuration
