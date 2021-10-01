resource "aws_lambda_function" "test_lambda1" {
  depends_on = [aws_cloudwatch_log_group.example1]

  function_name = "lambda_function_name_a"
  role          = "aws_iam_role.iam_for_lambda.arn"
  handler       = "exports.test"

  runtime = "nodejs12.x"
}

resource "aws_lambda_function" "test_lambda2" {
  depends_on = [aws_cloudwatch_log_group.example2]

  function_name = "lambda_function_name_b"
  role          = "aws_iam_role.iam_for_lambda.arn"
  handler       = "exports.test"

  runtime = "nodejs12.x"
}

resource "aws_lambda_function" "test_lambda3" {
  depends_on = [aws_cloudwatch_log_group.example3]

  function_name = "lambda_function_name_c"
  role          = "aws_iam_role.iam_for_lambda.arn"
  handler       = "exports.test"

  runtime = "nodejs12.x"
}

resource "aws_lambda_function" "test_lambda4" {
  function_name = "lambda_function_name_d"
  role          = "aws_iam_role.iam_for_lambda.arn"
  handler       = "exports.test"

  runtime = "nodejs12.x"
}

# If I omit this, the log group will be created automatically, but it won't have retention_in_days set to 90
resource "aws_cloudwatch_log_group" "example1" {
  name              = "lambda_function_name1"
  retention_in_days = 90
}

resource "aws_iam_role" "iam_for_lambda1" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


# If I omit this, the log group will be created automatically, but it won't have retention_in_days set to 90
resource "aws_cloudwatch_log_group" "example2" {
  name              = "lambda_function_name2"
  retention_in_days = 90
}

resource "aws_iam_role" "iam_for_lambda2" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


# If I omit this, the log group will be created automatically, but it won't have retention_in_days set to 90
resource "aws_cloudwatch_log_group" "example3" {
  name              = "lambda_function_name3"
  retention_in_days = 90
}

resource "aws_iam_role" "iam_for_lambda3" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


