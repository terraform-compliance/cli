Feature: Image scan to be enabled on push to ECR
  This feature will enforce vulnerabilty scan on images pushed to ECR

  IMPORTANT!
  This feature can not test the said vulnerability.
  kms_key_arn is only known after apply and won't be in the plan
  both enabled = false and enabled = true && not setting kms_key_arn results in server-side encryption being set to AWS owned CMK
  https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table#server_side_encryption

  Keeping this test for future reference

  Scenario: Image scan to be enabled on push.
    Given I have aws_dynamodb_table defined
    Then it must contain server_side_encryption
#     And it must contain kms_key_arn
