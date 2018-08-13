Feature: Resources should use encryption at rest while they are created
  In order to improve security
  As engineers
  We'll enforce encryption at rest

  Scenario: RDS instances
    When I define AWS RDS instance
    Then encryption must be enabled

  Scenario: EBS volumes
    When I define AWS EBS volume
    Then encryption must be enabled

  Scenario: S3 Buckets
    When I define AWS S3 Bucket
    Then it must contain server_side_encryption_configuration
