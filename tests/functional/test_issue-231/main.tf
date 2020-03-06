resource "aws_ecr_lifecycle_policy" "default" {
  repository = "blah"
  policy     = file("${path.module}/policy.json")
}
