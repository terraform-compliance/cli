provider "aws" {
  region = "us-east-1"
}

## Security Group for ELB
resource "aws_security_group" "failure" {
  name = "Failure_SG"
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "another_failure" {
  name = "Another-Failure_SG"
}

resource "aws_security_group_rule" "another_failure" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.another_failure.id
}