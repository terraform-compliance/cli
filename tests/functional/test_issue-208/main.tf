resource "aws_autoscaling_group" "thing" {
  name_prefix               = "thing"
  vpc_zone_identifier       = ["somesubnetid"]
  desired_capacity          = 3
  min_size                  = 1
  max_size                  = 3
  health_check_grace_period = 300
  health_check_type         = "EC2"
  force_delete              = true
  launch_configuration      = "someconfig"
  placement_group           = "somegroup"

  timeouts {
    delete = "15m"
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = [{
    key                 = "Name"
    value               = "thing"
    propagate_at_launch = true
  }, {
    key                 = "Environment"
    value               = "dev"
    propagate_at_launch = true
  }, {
    key                 = "Capability"
    value               = "thing"
    propagate_at_launch = true
  }]
}
