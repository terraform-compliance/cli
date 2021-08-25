//resource "aws_sns_topic" "should_pass" {
//  kms_master_key_id = aws_kms_key.should_pass.id
//}

resource "aws_kms_key" "should_pass" {
  description = "should pass"
}
//
//module "module_without_var" {
//  source = "./module_without_var"
//}

module "module_with_var" {
  source = "./module_with_var"
  kms_key_id = aws_kms_key.should_pass.id
}