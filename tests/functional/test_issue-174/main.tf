provider "aws" {
  region  = "eu-west-1"
}

resource "aws_s3_bucket" "b" {
  bucket = "my_test_bucket"
}

resource "aws_s3_bucket" "c" {
  bucket = "my_test_bucket_noncompliant"
}

resource "aws_s3_bucket_policy" "b" {
  bucket = "${aws_s3_bucket.b.id}"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "Bucket Policy",
  "Statement": [
      {
          "Sid": "Only allow SSL/TLS access",
          "Effect": "Deny",
          "Principal": "*",
          "Action": "s3:*",
          "Resource": "arn:aws:s3:::/*",
          "Condition": {
              "Bool": {
                  "aws:SecureTransport": "false"
              }
          }
      },
      {
          "Sid": "Only allow SSL/TLS access",
          "Effect": "Allow",
          "Principal": "*",
          "Action": "s3:*",
          "Resource": "arn:aws:s3:::/*"
      }
  ]
}
POLICY
}

resource "aws_s3_bucket_policy" "c" {
  bucket = "${aws_s3_bucket.c.id}"

  policy = <<POLICY2
{
  "Version": "2012-10-17",
  "Id": "Bucket Policy",
  "Statement": [
      {
          "Sid": "Allow S3 access",
          "Effect": "Allow",
          "Principal": "*",
          "Action": "s3:*",
          "Resource": "arn:aws:s3:::/*"
      },
      {
          "Sid": "Allow EC2 actions",
          "Effect": "Allow",
          "Principal": "*",
          "Action": "ec2:*",
          "Resource": "*"
      }
  ]
}
POLICY2
}

