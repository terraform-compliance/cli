variable "aws_region" {
  default = "eu-west-1"
}

variable "project" {
  default = "terraform-compliance"
}

variable "environment" {
  default = "test"
}

variable "application" {
  default = "156"
}

variable "SSH_PUB" {
  default = "some_public_ssh_key"
}

variable "SSH_PRI" {
  default = "some_private_ssh_key"
}



provider "aws" {
  region = "${var.aws_region}"

}

resource "aws_key_pair" "deployer" {
  key_name   = "${var.project}-${var.environment}-${var.application}-SSHKey-GitLab"
  public_key = "${var.SSH_PUB}"

}



resource "aws_security_group" "instance" {
  name = "terraform-example-instance"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["1.2.3.4/32"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["1.2.3.4/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_all"
  }

}



resource "aws_instance" "demo-prod-AppOne" {
  ami           = "ami-04b762b4289fba92b"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instance.id]
  key_name = "${var.project}-${var.environment}-${var.application}-SSHKey-GitLab"
  iam_instance_profile = "EC2-S3-READONLY"
  user_data = <<-EOF
#!/bin/bash
yum update -y
amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
yum install -y httpd mariadb-server
systemctl start httpd
systemctl enable httpd
usermod -a -G apache ec2-user
chown -R ec2-user:apache /var/www
chmod 2775 /var/www
find /var/www -type d -exec chmod 2775 {} \;
find /var/www -type f -exec chmod 0664 {} \;
echo "<?php phpinfo(); ?>" > /var/www/html/phpinfo.php
cat /tmp/index.php > /var/www/html/index.php
EOF

  provisioner "file" {
    source      = "./app/index.php"
    destination = "/tmp/index.php"
    connection {
      type = "ssh"
      user = "ec2-user"
      private_key = "${var.SSH_PRI}"
      host = aws_instance.demo-prod-AppOne.public_ip
    }
  }

  tags = {
    Name        = "${var.project}-${var.environment}-${var.application}",
    Env2         = "Prod"
  }
}



output "public_ip" {
  value       = aws_instance.demo-prod-AppOne.public_ip
  description = "The public IP of the web server"
}