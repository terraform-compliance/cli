provider "aws" {
  version = "~> 2.0"
}

provider "random" {
  version = "~> 2.0"
}

resource "aws_iam_role" "task" {
  name        = "${random_id.iam_prefix.hex}Task"
  description = "ECS task role for service"

  assume_role_policy = data.aws_iam_policy_document.ecs_assume_role.json

  tags = { Name = "ECS Task Role" }
}

resource "random_id" "iam_prefix" {
  byte_length = 8

  keepers = {
    name = var.name
  }
}

data "aws_iam_policy_document" "ecs_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

variable "name" {
  default = "test"
}