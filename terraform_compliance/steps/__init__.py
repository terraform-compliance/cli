

untaggable_resources = [
    "aws_route_table",
    "aws_route",
    "aws_main_route_table_association",
    "aws_elastic_beanstalk",
    "aws_elasticsearch_domain_policy",
    "aws_security_group_rule",
    "aws_eip",
    "aws_nat_gateway",
    "aws_egress_only_internet_gateway",
    "aws_key_pair",
    "aws_lambda",
    "aws_iam",
    "aws_s3_bucket_notification",
    "aws_api_gateway",
    "aws_cloudfront_origin_access_identity",
    "aws_cloudwatch",
    "aws_server_certificate",
    "aws_route53_record",
    "aws_directory_service_directory",
    "azurerm_resource_group",
    "aws_efs_mount_target",
    "aws_ecs_cluster",
    "aws_launch_configuration",
    "aws_kms_alias",
    "aws_kinesis_firehose_delivery_stream",
    "aws_vpc_dhcp_options_association",
    "null_resource",
    "random_string"
]

encryption_property = {
    "aws_db_instance": "storage_encrypted",
    "ebs_block_device": "encrypted",
    "aws_ebs_volume": "encrypted",
    "azurerm_storage_account": "enable_blob_encryption",
    "azurerm_sql_database": "encryption"
}

resource_name = {
    "AWS Auto-Scaling Group": "aws_autoscaling_group",
    "AWS EBS volume": "aws_ebs_volume",
    "AWS EC2 instance": "aws_instance",
    "AWS EFS file system": "aws_efs_file_system",
    "AWS ELB resource": "aws_elb",
    "AWS Internet Gateway": "aws_internet_gateway",    
    "AWS Launch Configuration": "aws_launch_configuration",
    "AWS RDS instance": "aws_db_instance",
    "AWS Route Table": "aws_route_table",
    "AWS S3 Bucket": "aws_s3_bucket",
    "AWS Security Group": "aws_security_group",
    "AWS VPC": "aws_vpc",
    "Azure SQL Database": "azurerm_sql_database",
    "Azure Storage Account": "azurerm_storage_account",
    "AWS Subnet": "aws_subnet",
    "resource that supports tags": "(?!{0}).*".format("|".join(untaggable_resources))
}
