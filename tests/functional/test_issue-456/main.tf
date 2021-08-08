module "ecr_repository_with_for" {
  source   = "./modules/ecr_module"
  for_each = var.ecr_repositories

  name          = each.key
  scan_on_push  = each.value.scan_on_push
}

module "ecr_repository_with_count" {
 source   = "./modules/ecr_module"
 count = 3

 name          = "bar"
 scan_on_push  = true
}

module "other_ecr_repository" {
  source   = "./modules/other_ecr_module"

  name                 = "non_for_loop_bar"
  scan_on_push = true
}

module "other_ecr_repository_with_count" {
 source   = "./modules/other_ecr_module"
 count = 7

 name          = "bar"
 scan_on_push  = true
}


# make sure "source" doesn't bleed into other non-module repositories

resource "aws_ecr_repository" "nonmodulerepository" {
  name                 = "non_module_bar"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# Resources to make sure the process of pulling the "source" doesn't break when not needed

resource "aws_iam_role" "test_iam_role" {
  for_each           = var.ecr_repositories
  name               = module.ecr_repository_with_for[each.key].not_ecr_name
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

resource "aws_instance" "server" {
  count = 2

  ami           = "ami-a1b2c3d4"
  instance_type = "t2.micro"

  tags = {
    Name = "Server ${count.index}"
  }
}

resource "aws_s3_bucket" "nonmodulebucket" {
  bucket = "nonmodule-bucket"
  acl    = "private"

  tags = {
    Name        = "My bucket1"
    Environment = "Dev"
  }
}