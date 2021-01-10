provider "aws" {
  region = "us-east-1"
}

resource "aws_rds_cluster" "db_cluster" {
  cluster_identifier      = "aurora-cluster-demo"
  engine                  = "aurora-postgresql"
  database_name           = "mydb"
  master_username         = "postgres"
  master_password         = "nothing"
  # kms_key_id = "arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"
  kms_key_id = null
}