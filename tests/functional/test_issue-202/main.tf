resource "aws_s3_bucket" "success" {
  bucket = "this-must-fail"
  acl = "private"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}

resource "aws_s3_bucket" "fail" {
  bucket = "this-must-fail"
  acl = "public"
}