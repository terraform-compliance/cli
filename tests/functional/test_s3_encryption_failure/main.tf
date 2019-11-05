resource "aws_s3_bucket" "fail" {
  bucket = "some_random_bucket_name-123808h0i1h3085018g531"
  acl    = "private"

  # There is no encryption for s3 here, so it must fail
}
