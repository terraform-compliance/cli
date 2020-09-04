resource "aws_security_group" "allow_ping" {
  name = "allow_ping"
  vpc_id = "vpc-12345678"
  ingress {
    protocol    = "icmp"
    from_port   = 8
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}