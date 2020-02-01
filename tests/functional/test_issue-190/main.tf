provider "aws" {
  region = "us-east-1"
}

module mysg {
  source = "./modules/secgroup"
}

## Security Group for ELB
resource "aws_security_group" "elb" {
  name = "Terraform-example-elb"
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    # cidr_blocks = ["0.0.0.0/0"]
    cidr_blocks = ["10.0.0.0/8"]
  }

  #   tags = module.tagsmod.tags
  #   tags = module.label.tags
  tags = {
    Name = "allow_all"
    role = "sgrole"
    BusinessUnit = "IT"
  }
}

resource "aws_security_group_rule" "elb-ingress-ssh" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  # security_group_id = aws_security_group.elb.id
  security_group_id = module.mysg.sg_id
}