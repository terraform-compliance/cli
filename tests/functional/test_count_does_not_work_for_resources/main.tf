resource "aws_vpc" "web_vpc" {
  cidr_block = "10.0.0.0/16" #var.web_vpc_cidr_block
  tags = merge(
  { "Name" = "vpc-testbla-13" },
  {} # var.common_tags
  )
}