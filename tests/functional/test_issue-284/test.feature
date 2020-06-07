Feature: Feature for issue 284
	In order to something
	As engineers
	We'll enforce something else

	Scenario Outline: Ensure S3 Bucket's ACL grant does not include write permissions, test2
		Given I have aws_s3_bucket defined
		When it has grant
		And its permissions does not include <value>
	Examples:
	| value           |
	| WRITE_ACP       |
	| WRITE_bidi      |
	| FULL_CONTROL_d  |
	| Something_bad	  |