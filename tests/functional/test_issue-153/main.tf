resource "aws_ebs_volume" "success" {
  availability_zone = "eu-west-1"
  size              = 40
}

resource "aws_ebs_volume" "fail" {
  availability_zone = "eu-west-1"
  size              = 50
}