resource "aws_s3_bucket" "a" {
  bucket = "my-tf-test-bucket"
  tags = {
    MyBuggyTag = "none"
    MyOkTag    = "ok"
  }
}

resource "aws_s3_bucket" "b" {
  bucket = "my-tf-test-bucket"
  tags = {
    MyBuggyTag = ""
    MyOkTag    = "ok"
  }
}


resource "aws_s3_bucket" "c" {
  bucket = "my-tf-test-bucket"
}