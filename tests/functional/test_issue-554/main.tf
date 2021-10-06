resource "aws_vpc" "fail" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_security_group_rule" "pass" {
  type        = "ingress"
  from_port   = 1
  to_port     = 1
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = "sg-123456"
}

resource "aws_security_group_rule" "fail" {
  type        = "egress"
  from_port   = 2
  to_port     = 2
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = "sg-123456"
}


resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.fail.id
}
