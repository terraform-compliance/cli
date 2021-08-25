resource "aws_sns_topic" "this" {
  kms_master_key_id = aws_kms_key.this.id
}

resource "aws_kms_key" "this" {
  description = "kms key created in module without var"
}

