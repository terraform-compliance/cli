provider "aws" {
  region  = "eu-west-1"
}

# ----------------------------------------------------------------
# Data sources
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Helper Resources needed to provision some of the test Resources
# ----------------------------------------------------------------
resource "aws_vpc" "test-vpc" {
  cidr_block       = "10.0.0.0/16"

  tags = {
    Name = "TestVPC Compliant checks"
  }
}

resource "aws_internet_gateway" "test-igw" {
  vpc_id = "${aws_vpc.test-vpc.id}"

  tags = {
    Name = "Test VPC IGW"
  }
}

resource "aws_subnet" "test-subnet-pubA" {
  vpc_id     = "${aws_vpc.test-vpc.id}"
  cidr_block = "10.0.0.0/24"

  tags = {
    Name = "Public Subnet A Compliant checks"
  }
}

resource "aws_subnet" "test-subnet-pubB" {
  vpc_id     = "${aws_vpc.test-vpc.id}"
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "Public Subnet B Subnet Compliant checks"
  }
}

resource "aws_subnet" "test-subnet-privA" {
  vpc_id     = "${aws_vpc.test-vpc.id}"
  cidr_block = "10.0.10.0/24"

  tags = {
    Name = "Private Subnet A Subnet Compliant checks"
  }
}

resource "aws_subnet" "test-subnet-privB" {
  vpc_id     = "${aws_vpc.test-vpc.id}"
  cidr_block = "10.0.11.0/24"

  tags = {
    Name = "Private Subnet B Compliant checks"
  }
}

resource "aws_route_table" "test-pub-rtb" {
  vpc_id = "${aws_vpc.test-vpc.id}"

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.test-igw.id}"
  }

  tags = {
    Name = "Test VPC Public Route Table"
  }
}

resource "aws_route_table_association" "test-pubA-rtb-assoc" {
  subnet_id      = "${aws_subnet.test-subnet-pubA.id}"
  route_table_id = "${aws_route_table.test-pub-rtb.id}"
}

resource "aws_route_table_association" "test-pubB-rtb-assoc" {
  subnet_id      = "${aws_subnet.test-subnet-pubB.id}"
  route_table_id = "${aws_route_table.test-pub-rtb.id}"
}

# ----------------------------------------------------------------
# Compliant
# ----------------------------------------------------------------
# Create Loadbalancer with listener on port 443 and redirect on port 80 to 8080
# [1] Security Group
resource "aws_security_group" "sg-loadBalancer-noncompliant" {
  name        = "sg-loadBalancer-noncompliant"
  description = "Allow HTTP/HTTPS inbound traffic"
  vpc_id      = "${aws_vpc.test-vpc.id}"

  ingress {
    # HTTP (change to whatever ports you need)
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    # HTTPS
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}


# Network LoadBalancer
resource "aws_lb" "nlb-noncompliant" {
  name               = "nlb-noncompliant"
  internal           = false
  load_balancer_type = "network"
  security_groups    = ["${aws_security_group.sg-loadBalancer-noncompliant.id}"]
  subnets            = ["${aws_subnet.test-subnet-pubA.id}",
    "${aws_subnet.test-subnet-pubB.id}"]
}

# [1] Listener on TCP on port other then 443
resource "aws_lb_listener" "tcp-listener-noncompliant" {
  load_balancer_arn = "${aws_lb.nlb-noncompliant.arn}"
  port              = "80"
  protocol          = "TCP"

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "HEALTHY"
      status_code  = "200"
    }
  }
}

# [2] Listener on UDP
resource "aws_lb_listener" "udp-listener-noncompliant" {
  load_balancer_arn = "${aws_lb.nlb-noncompliant.arn}"
  port              = "1443"
  protocol          = "UDP"

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "HEALTHY"
      status_code  = "200"
    }
  }
}

# [3] Listener on TCP_UDP
resource "aws_lb_listener" "tcpudp-listener-noncompliant" {
  load_balancer_arn = "${aws_lb.nlb-noncompliant.arn}"
  port              = "53"
  protocol          = "TCP_UDP"

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "HEALTHY"
      status_code  = "200"
    }
  }
}