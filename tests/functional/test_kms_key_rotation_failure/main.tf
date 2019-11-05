resource "aws_kms_key" "test-fail-key" {
  description             = "KMS Key for failure test"
  deletion_window_in_days = 7
}
