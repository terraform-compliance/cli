module "ecr_repository" {
  source   = "./modules/ecr_module"
  name          = var.repo_name
  scan_on_push  = var.scan_on_push_val
}


resource "aws_iam_role" "test_iam_role" {
  name               = module.ecr_repository.ecr_name
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

provider "aws" {
  region  = "us-east-1"
}