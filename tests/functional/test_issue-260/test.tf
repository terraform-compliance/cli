resource "aws_sqs_queue" "success" {
  kms_master_key_id = "key"
}

resource "aws_sqs_queue" "failure" {
  kms_master_key_id = aws_kms_key.test.id
}
resource "aws_kms_key" "test" {
  description         = "test"
  enable_key_rotation = true
}