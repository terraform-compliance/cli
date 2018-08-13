Feature: Resources should be encrypted
  In order to improve security
  As engineers
  We'll enforce encryption

  Scenario: RDS instances
    When I define a AWS RDS instance
    Then encryption must be enabled

  Scenario: EBS volumes
    When I define a AWS EBS volume
    Then encryption must be enabled

  Scenario: S3 Buckets
    When I define a AWS S3 Bucket
    Then it must contain server_side_encryption_configuration
