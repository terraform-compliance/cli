resource "aws_sns_topic" "test" {
  name = "my-topic-with-policy"
}

resource "" "default" {
  arn = aws_sns_topic.test.arn

  policy =<<POLICY
  
  {
  "Statement": [{
    "Sid": "Statement1",
    "Effect": "Allow",
    "Principal": {
      "AWS": "111122223333"
    },
    "Action": ["sns:Subscribe"],
    "Resource": "arn:aws:sns:us-east-2:444455556666:MyTopic",
    "Condition": {
      "StringEquals": {
        "sns:Protocol": "https"
      }
    }
  }]
}
POLICY  
}