module "inner" {
  source = "./inner"
}

resource "aws_lambda_permission" "example" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "example-fn"
  principal     = "events.amazonaws.com"
  source_arn    = module.inner.event_rule_arn
}
