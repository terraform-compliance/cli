module "outer" {
  source = "./outer"
}

resource "null_resource" "example" {
  triggers = {
    value = module.outer.forwarded_value
  }
}
