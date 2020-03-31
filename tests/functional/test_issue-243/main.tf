resource "aws_s3_bucket" "success" {
  bucket = "succeeded-bucket"

  tags = {
    environment = "live"
    service = "some service"
  }
}

resource "aws_s3_bucket" "skip" {
  bucket = "skipped-bucket"

  tags = {
    something = "something else"
  }
}

resource "aws_s3_bucket" "another_skip" {
  bucket = "skipped-bucket-2"

  tags = {
    environment = "dead"
    something = "something else"
  }
}

resource "aws_s3_bucket" "failure" {
  bucket = "failed-bucket"

  tags = {
    environment = "live"
    some_other_tag = "something"
  }
}

resource "aws_s3_bucket" "another_failure" {
  bucket = var.bucket_name

  tags = {
    environment = "live"
    service = ""
  }
}


variable "bucket_name" {
  default = "test"
}

resource "aws_autoscaling_group" "success" {
  name = "test"
  min_size = 1
  max_size = 1

  tag {
    key = "environment"
    value = "live"
    propagate_at_launch = true
  }
  tag {
    key = "service"
    value = "some_service"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_group" "skipped" {
  name = "test"
  min_size = 1
  max_size = 1

  tag {
    key = "environment"
    value = "dead"
    propagate_at_launch = true
  }
  tag {
    key = "service"
    value = "some_service"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_group" "failure_1" {
  name = "test_1"
  min_size = 1
  max_size = 1

  tag {
    key = "environment"
    value = "live"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_group" "failure_2" {
  name = "test_2"
  min_size = 1
  max_size = 1

  tag {
    key = "environment"
    value = "live"
    propagate_at_launch = true
  }
  tag {
    key = "service"
    value = ""
    propagate_at_launch = true
  }
}