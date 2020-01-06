resource "aws_security_group" "alb" {
  name   = "submodule-sg"
  vpc_id = "vpc-12345"

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    # cidr_blocks = ["0.0.0.0/0"]
    cidr_blocks = ["10.0.0.0/8"]
  }

  lifecycle {
    create_before_destroy = true
  }
}