resource "aws_sns_topic" "this" {
  kms_master_key_id = var.kms_key_id
}

variable "kms_key_id" {}

