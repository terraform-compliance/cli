provider "aws" {
  region = "us-east-1"
}

#### valid

resource "aws_security_group" "valid" {
  name        = "AppTier-app-sg"
  description = "Allow TLS inbound traffic"
  vpc_id      = "vpc-12345678"

  ingress {
    description = "TLS from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.1.1.0/24"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.1.1.0/24"]
  }

  tags = {
    Name = "valid-sg",
    Tier = "apptier"
  }
}

resource "aws_launch_configuration" "valid" {
  name_prefix          = "terraform-lc-example"
  image_id             = "ami-9999ffff5555ffff1"
  instance_type        = "t2.micro"
  security_groups      = [aws_security_group.valid.id]
  iam_instance_profile = "webtier-test"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "valid" {
  name                      = "loadbalancer-terraform-test"
  max_size                  = 5
  min_size                  = 2
  health_check_grace_period = 300
  health_check_type         = "ELB"
  desired_capacity          = 4
  force_delete              = true
  launch_configuration      = aws_launch_configuration.valid.name
  vpc_zone_identifier       = ["vpc-12345678"]

  initial_lifecycle_hook {
    name                 = "foobar"
    default_result       = "CONTINUE"
    heartbeat_timeout    = 2000
    lifecycle_transition = "autoscaling:EC2_INSTANCE_LAUNCHING"

    notification_metadata = <<EOF
{
  "foo": "bar"
}
EOF

    notification_target_arn = "arn:aws:sqs:us-east-1:444455556666:queue1*"
    role_arn                = "arn:aws:iam::123456789012:role/S3Access"
  }

  tag {
    key                 = "foo"
    value               = "bar"
    propagate_at_launch = true
  }

  timeouts {
    delete = "15m"
  }

  tag {
    key                 = "Tier"
    value               = "apptier"
    propagate_at_launch = false
  }
}
