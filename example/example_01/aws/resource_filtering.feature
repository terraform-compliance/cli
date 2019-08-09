Feature: Resource Filtering example

  Scenario Outline: Ensure that extra tags are defined and match regex for S3 Buckets
    Given I have AWS S3 Bucket defined
    When its address is aws_s3_bucket.s3_bucket_prod
    And it contains tags
    Then it must contain <tag_keys>
    And its value must be <string>

    Examples:
      | tag_keys            | string |
      | Data Classification | PRIVATE                 |
      | Data Residency      | EU                      |
