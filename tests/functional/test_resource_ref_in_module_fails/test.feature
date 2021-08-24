Feature: test

  Scenario: Reject if a S3 bucket allows public access
        Given I have aws_s3_bucket defined
        Then aws_s3_bucket_public_access_block must be enabled
        And block_public_acls must be enabled
        And ignore_public_acls must be enabled
        And block_public_policy must be enabled
        And restrict_public_buckets must be enabled