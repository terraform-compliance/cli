resource "aws_rds_cluster" "db_cluster" {
  cluster_identifier      = "aurora-cluster-demo"
  engine                  = "aurora-postgresql"
  database_name           = "mydb"
  master_username         = "postgres"
  master_password         = "nothing"
}
