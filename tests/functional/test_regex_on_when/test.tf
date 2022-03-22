terraform {
  required_providers {
    aws = {
      version = "4.6.0"
      source = "hashicorp/aws"
    }
  }
}

resource "aws_s3_bucket" "bucket" {
  bucket = "test-bucket" 
}

#resource "aws_s3_bucket_versioning" "versioning" {
#  bucket = aws_s3_bucket.bucket.id
#  versioning_configuration {
#    status = "Enabled"
#  }
#}

module "project1" {
  source = "./module"
}