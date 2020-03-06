resource "aws_lb" "internal" {
  name               = "test-alb"
  internal           = true
  load_balancer_type = "application"

  subnets                          = ["test"]
  enable_cross_zone_load_balancing = true
}
