module "ecr_repository" {
  source   = "modules\/ecr_module"
  for_each = var.ecr_repositories

  name          = each.key
  scan_on_push  = each.value.scan_on_push
}


resource "aws_iam_role" "test_iam_role" {
  for_each           = var.ecr_repositories
  name               = module.ecr_repository[each.key].ecr_name
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
