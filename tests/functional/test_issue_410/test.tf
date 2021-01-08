resource "aws_instance" "ebs_encrypted_not_present" {
  ami               = "ami-003634241a8fcdec0"
  instance_type     = "t2.medium"
  key_name          = "tfcompliance_inf"
  security_groups   = []

  root_block_device {
    volume_size = 200
    volume_type = "gp2"
    encrypted   = true
  }

  ebs_block_device {
    device_name           = "/dev/sdg"
    volume_size           = 50
    volume_type           = "gp2"
    delete_on_termination = true
  }

  tags = {
    budget-area = "security"
    group       = "Cybersecurity"
  }
}
