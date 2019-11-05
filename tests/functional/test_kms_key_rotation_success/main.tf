resource "aws_kms_key" "test-key" {
  description             = "KMS Key for test"
  deletion_window_in_days = 7
  enable_key_rotation     = true
}
