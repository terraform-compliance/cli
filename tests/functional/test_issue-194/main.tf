provider "aws" {
  region                      = "us-west-2"
  version                     = "~> 2.43"
}

resource "aws_instance" "one" {
  ami           = "ami-6d1c2007"
  instance_type = "t2.micro"

  network_interface {
    device_index         = 1
    network_interface_id = "eth0"
  }
}

resource "aws_instance" "two" {
  ami           = "ami-6d1c2007"
  instance_type = "t2.micro"

  network_interface {
    device_index         = 1
    network_interface_id = "eth0"
  }

  network_interface {
    device_index         = 2
    network_interface_id = "eth1"
  }
}