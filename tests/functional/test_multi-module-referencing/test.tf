module "first_layer" {
  source = "./module1"
}

provider "aws" {
  region = "eu-west-1"
}