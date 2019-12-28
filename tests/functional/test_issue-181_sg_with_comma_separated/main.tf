resource "aws_security_group" "allow_tls_ingress_inline" {
  name        = "allow_tls_ingress_inline"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 53
    to_port     = 53
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "something_else" {
  name = "Some_other_sg"
}

resource "aws_security_group_rule" "port_80" {
  type = "ingress"
  protocol = "tcp"
  from_port = 80
  to_port = 80
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = aws_security_group.something_else.id
}

resource "aws_security_group_rule" "port_53" {
  type = "ingress"
  protocol = "tcp"
  from_port = 53
  to_port = 53
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = aws_security_group.something_else.id
}
