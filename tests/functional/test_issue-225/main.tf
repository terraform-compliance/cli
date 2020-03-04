module "appmesh_existing" {
  source = "./appmesh"
}

provider "aws" {
  region = "eu-west-1"
}