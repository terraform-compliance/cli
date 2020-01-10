resource "aws_kms_key" "test" {
  description = "Test"
}

output "string" {
  value = "Something"
}

output "list" {
  value = ["something", "else"]
}

output "map" {
  value = {
    something="else"
  }
  sensitive = true
}

output "resource_object_ref" {
  value = aws_kms_key.test
}

output "resource_parameter_ref" {
  value = aws_kms_key.test.key_id
}
