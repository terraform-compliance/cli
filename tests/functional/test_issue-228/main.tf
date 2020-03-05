provider "aws" {
  access_key = "foo"
  secret_key = "bar"
  skip_credentials_validation = true
  skip_requesting_account_id = true
  region = "eu-west-2"
}

resource "aws_s3_bucket" "bucket" {
    bucket = "bucket"

    tags = {
        Colour = "Red"
    }
}