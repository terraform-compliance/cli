Feature: All AWS environments that has S3 Bucket Public Access Block
  Must have enabled on defined directives

  Scenario Outline: AWS Credentials should not be hardcoded
    Given I have aws_s3_bucket_public_access_block resource configured
    Then it must contain <key>
    And its value must match the "true" regex

    Examples:
    | key                      |
    | block_public_acls        |
    | block_public_policy      |
    | ignore_public_acls       |
    | restrict_public_buckets  |
