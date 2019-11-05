Feature: Default S3 bucket encryption must be set to SSE-KMS
    This feature checks if any S3 bucket is defined without default encryption.
    The check does not check S3 bucket with public read ACL hosting static website.
    Scenario: Reject if an S3 bucket is not encrypted
        Given I have AWS S3 Bucket defined
        Then it must contain server_side_encryption_configuration
