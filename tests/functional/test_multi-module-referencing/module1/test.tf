module "second_layer" {
  source = "module2"
}

resource "aws_s3_bucket" "should_not_fail_first_layer" {
  bucket = "some-test-bucket-should_not_fail_first_layer"
}

resource "aws_s3_bucket_public_access_block" "should_not_fail_first_layer" {
  bucket = aws_s3_bucket.should_not_fail_first_layer.bucket
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
