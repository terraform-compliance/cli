resource "aws_security_group" "alb" {
  name        = "alb-sg"
  description = "Act as identifier of this ALB to be used as source security group in other rules. Allows outbound traffic back to origin network"
  vpc_id = var.vpc_id
}

resource "aws_security_group_rule" "alb_ingress_self" {
  type            = "ingress"
  description     = "Allow ALB to communicate with itself (ingress)"
  security_group_id = aws_security_group.alb.id
  protocol        = "tcp"
  from_port       = 0
  to_port         = 65535
  self            = true
}

resource "aws_security_group_rule" "alb_egress_self" {
  type            = "egress"
  description     = "Allow ALB to communicate with itself (egress)"
  security_group_id = aws_security_group.alb.id
  protocol        = "tcp"
  from_port       = 0
  to_port         = 65535
  self            = true
}

resource "aws_security_group" "alb_ecs" {
  name        = "alb-ecs-access"
  description = "Allow ALB access to ECS task(s)"
  vpc_id = var.vpc_id
}

resource "aws_security_group_rule" "alb_ecs_ingress" {
  type            = "ingress"
  description     = "Allow ALB to communicate with ECS tasks on port 8080"
  security_group_id = aws_security_group.alb_ecs.id
  protocol        = "tcp"
  from_port       = 8080
  to_port         = 8080
  source_security_group_id = aws_security_group.alb.id
}

variable "vpc_id" {
  default = "test_vpc"
}