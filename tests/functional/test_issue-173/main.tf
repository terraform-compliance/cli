provider "aws" {
  region = "${var.region}"
}

provider "aws" {
  region = "us-west-2"
  alias  = "should-fail"
  access_key = "AKIAIOSFODNN7EXAMPLE"
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}