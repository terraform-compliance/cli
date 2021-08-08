provider "aws" {
  region = "us-west-1"
}

module "ecr_repository" {
  source   = "modules\/ecr_module"
  for_each = var.ecr_repositories

  name          = each.key
  scan_on_push  = each.value.scan_on_push
}
