resource "aws_vpc" "test" {
  cidr_block = "10.103.0.0/16"
  tags = {
    Name = "mcrilly-sandbox"
    Environment = "Sandbox"
  }
}

resource "aws_subnet" "test" {
  cidr_block = "10.103.1.0/24"
  vpc_id = aws_vpc.test.id
}