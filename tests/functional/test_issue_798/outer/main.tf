module "inner" {
  source = "./inner"
}

output "forwarded_value" {
  value = module.inner.value
}
