property_match_list = {
    'encryption at rest': {
        'aws_db_instance': 'storage_encrypted',
        'ebs_block_device': 'encrypted',
        'aws_ebs_volume': 'encrypted',
        'azurerm_storage_account': 'enable_blob_encryption',
        'azurerm_sql_database': 'encryption',
        'aws_s3_bucket': 'server_side_encryption_configuration',
        'aws_elasticache_replication_group': 'at_rest_encryption_enabled',
        'aws_emr_security_configuration': 'EnableAtRestEncryption'
    },
    'encryption in flight': {
        'aws_elasticache_replication_group': 'transit_encryption_enabled',
        'aws_emr_security_configuration': 'EnableInTransitEncryption'
    }
}

resource_name = {
    'AWS Auto-Scaling Group': 'aws_autoscaling_group',
    'AWS EBS volume': 'aws_ebs_volume',
    'AWS EC2 instance': 'aws_instance',
    'AWS EFS file system': 'aws_efs_file_system',
    'AWS ELB resource': 'aws_elb',
    'AWS EMR Security Configuration': 'aws_emr_security_configuration',
    'AWS Internet Gateway': 'aws_internet_gateway',
    'AWS Launch Configuration': 'aws_launch_configuration',
    'AWS RDS instance': 'aws_db_instance',
    'AWS Route Table': 'aws_route_table',
    'AWS S3 Bucket': 'aws_s3_bucket',
    'AWS Security Group': 'aws_security_group',
    'AWS VPC': 'aws_vpc',
    'Azure SQL Database': 'azurerm_sql_database',
    'Azure Storage Account': 'azurerm_storage_account',
    'AWS Subnet': 'aws_subnet',
    'AWS ElastiCache Replication Group': 'aws_elasticache_replication_group',
    'AWS Elastic Cache Replication Group': 'aws_elasticache_replication_group'
}
