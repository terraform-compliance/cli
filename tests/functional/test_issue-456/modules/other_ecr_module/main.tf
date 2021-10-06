variable "name" {
  type = string
}

variable "scan_on_push" {
  type    = string
  default = true
}

resource "aws_ecr_repository" "ecr_repository" {
  name                 = var.name
  image_tag_mutability =  "IMMUTABLE" 

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }

}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "ecr_repository" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  tags = {
    Name = "HelloWorld"
  }
}

output "ecr_name" {
  value = aws_ecr_repository.ecr_repository.id
}

output "not_ecr_name" {
  value = 1234
}