resource "aws_s3_bucket" "test" {
  for_each = toset(["a"])
  bucket = "test-bucket"
}

resource "aws_s3_bucket_public_access_block" "test" {
  for_each = toset(["a"])
  bucket = aws_s3_bucket.test["a"].id
  block_public_acls = true
  block_public_policy = false
  ignore_public_acls = true
  restrict_public_buckets = true
}