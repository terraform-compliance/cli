

untaggable_resources = [
    "aws_route_table",
    "aws_elastic_beanstalk",
    "aws_security_group_rule",
    "aws_eip",
    "aws_nat_gateway",
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
    "azurerm_resource_group"
]

encryption_property = {
    "aws_db_instance": "storage_encrypted",
    "ebs_block_device": "encrypted",
    "aws_ebs_volume": "encrypted",
    "azurerm_storage_account": "enable_blob_encryption",
    "azurerm_sql_database": "encryption"
}

resource_name = {
    "AWS RDS instance": "aws_db_instance",
    "AWS EC2 instance": "aws_instance",
    "AWS EBS volume": "aws_ebs_volume",
    "AWS Security Group": "aws_security_group",
    "AWS Subnet": "aws_subnet",
    "Azure Storage Account": "azurerm_storage_account",
    "Azure SQL Database": "azurerm_sql_database",
    "resource that supports tags": "(?!{0}).*".format("|".join(untaggable_resources))
}

regex = {
    "Name": "^\${var.platform}_\${var.environment}_.*"
}
