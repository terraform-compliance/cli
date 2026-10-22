resource "aws_cloudwatch_event_rule" "example" {
  name                = "example"
  schedule_expression = "rate(15 minutes)"
}

output "event_rule_arn" {
  value = aws_cloudwatch_event_rule.example.arn
}
