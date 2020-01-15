resource "aws_route53_health_check" "url-health-check" {
  for_each          = toset(var.health_check_urls)
  fqdn              = each.value
  port              = 443
  type              = "HTTPS"
  failure_threshold = "1"
  request_interval  = "10"

}

resource "aws_cloudwatch_metric_alarm" "url-health-check-alarm" {
  for_each            = toset(var.health_check_urls)
  alarm_name          = "${each.value}-url-health-check"
  namespace           = "AWS/Route53"
  metric_name         = "HealthCheckStatus"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  period              = "60"
  statistic           = "Minimum"
  threshold           = "1"
  unit                = "None"

  dimensions = {
    HealthCheckId = aws_route53_health_check.url-health-check[each.value].id
  }
}

variable "health_check_urls" {
  type = list(string)
  description = "Testing"
  default = ["test.domain.com"]
}