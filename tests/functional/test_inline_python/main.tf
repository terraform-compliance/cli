resource "aws_vpc_peering_connection" "foo" {
  peer_owner_id = aws_vpc.bar.id
  peer_vpc_id   = aws_vpc.bar.id
  vpc_id        = aws_vpc.foo.id
  auto_accept   = true

  tags = {
    Name = "VPC Peering between foo and bar"
  }
}

resource "aws_vpc_peering_connection" "foo2" {
  peer_owner_id = aws_vpc.bar.id
  peer_vpc_id   = aws_vpc.foo.id
  vpc_id        = aws_vpc.bar.id
  auto_accept   = true

  tags = {
    Name = "VPC Peering between foo and bar"
  }
}

resource "aws_vpc" "foo" {
  cidr_block = "10.1.0.0/16"
}

resource "aws_vpc" "bar" {
  cidr_block = "10.2.0.0/16"
}