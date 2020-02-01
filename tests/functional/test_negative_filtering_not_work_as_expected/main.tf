resource "aws_ssm_parameter" "should_exist" {
  type = "String"
  name = "something"
  value = "something"
}

resource "aws_s3_bucket" "should_not_exist" {
  bucket = "something-else"
}
