module "test" {
  for_each = toset(["a", "b"])
  source = "./test_module"
}

module "test2" {
  source = "./test_module_2"
}