resource "aws_security_group" "ecs_task" {
  name        = "ecs-tasks"
  description = "Allow ECS Fargate tasks to communicate with each other"
  vpc_id      = var.vpc_id

  timeouts {
    create = "5m"
    delete = "5m"
  }
}

resource "aws_security_group_rule" "ecs_task_ingress_self" {
  type              = "ingress"
  description       = "Allow ECS task to communicate with itself (ingress)"
  security_group_id = aws_security_group.ecs_task.id
  protocol          = "tcp"
  from_port         = 0
  to_port           = 65535
  self              = true
}

resource "aws_security_group_rule" "ecs_task_egress_self" {
  type              = "egress"
  description       = "Allow ECS task to communicate with itself (egress)"
  security_group_id = aws_security_group.ecs_task.id
  protocol          = "tcp"
  from_port         = 0
  to_port           = 65535
  self              = true
}

resource "aws_security_group_rule" "ecs_task_egress_to_internet_443" {
  type              = "egress"
  description       = "Allow ECS task to communicate with Internet on 443"
  security_group_id = aws_security_group.ecs_task.id
  protocol          = "tcp"
  from_port         = 443
  to_port           = 443
  #tfsec:ignore:AWS007
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "ecs_task_egress_to_mssql" {
  type              = "egress"
  description       = "Allow ECS task to communicate with MSSQL"
  security_group_id = aws_security_group.ecs_task.id
  protocol          = "tcp"
  from_port         = 1433
  to_port           = 1433
  cidr_blocks       = ["10.0.0.0/16"]
}

variable "vpc_id" {
  default = "vpc_1235678"
}