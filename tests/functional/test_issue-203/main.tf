resource "aws_iam_role" "build_user_s3_dev" {
  name = "AWSBuildUserRole"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "something"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

}
