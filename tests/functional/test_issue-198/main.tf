resource "aws_security_group" "efs" {
  name        = "test-efs"
  description = "Test EFS Security Group"
  vpc_id      = "vpc-cc963da9"

}

resource "aws_security_group_rule" "efs_allow_all_outbound" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.efs.id
}

resource "aws_security_group_rule" "efs_access" {

  type                     = "ingress"
  description              = "access to EFS"
  from_port                = 2049
  to_port                  = 2049
  protocol                 = "tcp"
  source_security_group_id = "sg-0143f76c834026ebd"
  security_group_id        = aws_security_group.efs.id
}
