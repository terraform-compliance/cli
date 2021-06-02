esource "aws_s3_bucket" "fail" {
  bucket = "some_random_bucket_name-123808h0i1h3085018g531"
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = "123456"
        sse_algorithm     = "aws:kms"
      }
    }
  }
}
