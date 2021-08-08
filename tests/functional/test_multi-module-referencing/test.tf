module "first_layer" {
  source = "./module1"
}

module "root_layer" {
  source = "./module1"
}


provider "aws" {
  region = "eu-west-1"
}

resource "aws_s3_bucket" "no_module_boundary" {
  bucket = "some-test-bucket-no_module_boundary"
}

resource "aws_s3_bucket_public_access_block" "no_module_boundary" {
  bucket = aws_s3_bucket.no_module_boundary.bucket
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}