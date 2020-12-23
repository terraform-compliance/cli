---
layout: default
title: GIVEN Directives
nav_order: 1
has_children: false
parent: BDD Reference
---

# GIVEN

`GIVEN` directive is use to set the initial standard about the type of the entity that you are searching for.
Every Scenario must have a `GIVEN` as the first step defining the context.

If the scenario starts with `Given I have aws_s3_bucket defined`, the step below will have all the aws_s3_bucket resources defined in its context.


Few examples can be ;

```gherkin
Given I have AWS S3 Bucket defined
```

```gherkin
Given I have aws_s3_bucket defined
```

```gherkin
Given I have any resource defined
```

You can not use `AND` with `GIVEN`.

or depending on use a [Scenario Outline](/pages/bdd-references#Scenario) instead of a Scenario, it can also 
be a variable like ;

```gherkin
Given I have <resource_type> defined
```

## Reference
* Table of Contents
{:toc}

### [Given](#){: .p-1 .text-red-200} I have [name](#){: .text-green-200 .fw-700} [type](#){: .text-blue-100 .fw-700} configured


> __Possible sentences :__
>
> ▪
[Given](#){: .p-1 .text-red-200} 
I have 
[name](#){: .text-green-200 .fw-700} 
[type](#){: .text-blue-100 .fw-700} 
configured
>
| key | Description | Examples |
|:---:|:----------|:-|
| [name](#){: .text-green-200 .fw-700}  | name of the key in terraform. | `aws_security_group` `ingress`<br><br>In order to define all resources, you can also use ;<br><br>`a resource` `any resource` `a` `any` `anything` |
| [type](#){: .text-blue-100 .fw-700}  | The type of the key. | It can be one of these ;<br>`resource` `resources` `provider` `providers` `data` `datas` `variable` `variables` |

__Please note__, `Given I have any resource` can be used to capture all resources.
```
Given I have any resource defined
When its provider_name is aws
...
```
Will run following steps on all aws resources.



----------------------
### [Given](#){: .p-1 .text-red-200} I have [name](#){: .text-green-200 .fw-700} defined


> __Possible sentences :__
>
> ▪
[Given](#){: .p-1 .text-red-200} 
I have 
[name](#){: .text-green-200 .fw-700} 
defined
>
| key | Description | Examples |
|:---:|:----------|:-|
| [name](#){: .text-green-200 .fw-700}  | name of the resource. The name must point to a resource. Can not be `provider` or anything else. | `aws_security_group` `aws_s3_bucket` |



----------------------
### [Given](#){: .p-1 .text-red-200} I have resource that supports [something](#){: .p-1 .text-green-200 .fw-700}


> __Possible sentences :__
>
> ▪
[Given](#){: .p-1 .text-red-200} 
I resource that supports 
[something](#){: .p-1 .text-green-200 .fw-700}
>
| key | Description | Examples |
|:---:|:----------|:-|
| [something](#){: .p-1 .text-green-200 .fw-700}  | [something](#){: .p-1 .text-green-200 .fw-700} | any property within Terraform resource/provider/etc | `tags` `access_key` `ingress` `"something with spaces"` `kms_key_id` |

NOTE: Some properties will act different than others based on if they are a default property as determined by Terraform. Default properties for a will be found in has and must contain clauses even if they are null and so must be checked for null status as in [Examples about tags](/pages/Examples/tags_related.html). The non-default values as described below will be found when using this 'supports [something](#){: .p-1 .text-green-200 .fw-700}' statement, but will not be found in the given resource unless the property has been defined in the Terraform config.

Default properties in this instance are properties which show up in the plans json file in the resources 'values' key even when that property is not included in the Terraform configuration. An example of a Terraform default property for an AWS RDS Cluster is shown below.

Simple AWS RDS Cluster configuration
```hcl
resource "aws_rds_cluster" "db_cluster" {
  cluster_identifier      = "aurora-cluster-demo"
  engine                  = "aurora-postgresql"
  database_name           = "mydb"
  master_username         = "postgres"
  master_password         = "nothing"
}
```

The matching resource in the plan.json is:
```json
{
    "format_version": "0.1",
    "terraform_version": "0.14.2",
    "planned_values": {
        "root_module": {
            "resources": [
                {
                    "address": "aws_rds_cluster.db_cluster",
                    "mode": "managed",
                    "type": "aws_rds_cluster",
                    "name": "db_cluster",
                    "provider_name": "registry.terraform.io/hashicorp/aws",
                    "schema_version": 0,
                    "values": {
                        "allow_major_version_upgrade": null,
                        "backtrack_window": null,
                        "backup_retention_period": 1,
                        "cluster_identifier": "aurora-cluster-demo",
                        "copy_tags_to_snapshot": false,
                        "database_name": "mydb",
                        "deletion_protection": null,
                        "enable_http_endpoint": false,
                        "enabled_cloudwatch_logs_exports": null,
                        "engine": "aurora-postgresql",
                        "engine_mode": "provisioned",
                        "final_snapshot_identifier": null,
                        "global_cluster_identifier": null,
                        "iam_database_authentication_enabled": null,
                        "iam_roles": null,
                        "master_password": "nothing",
                        "master_username": "postgres",
                        "replication_source_identifier": null,
                        "restore_to_point_in_time": [],
                        "s3_import": [],
                        "scaling_configuration": [],
                        "skip_final_snapshot": false,
                        "snapshot_identifier": null,
                        "source_region": null,
                        "tags": null,
                        "timeouts": null
                    }
                }
            ]
        }
    },
```

We know that AWS RDS Clusters can use KMS Keys for encryption, but there are not included in this 'values' section in the plan unless they are specifically called out. In this case a has or must contain statement will not find kms_key_id in this example cluster. 

Supported, but non-default properties show up in a different section of the json file (resource_changes.[].change.after_unknown). Below is the relevant section in the plan.json file referenced above:

```json
    "resource_changes": [
        {
            "address": "aws_rds_cluster.db_cluster",
            "mode": "managed",
            "type": "aws_rds_cluster",
            "name": "db_cluster",
            "provider_name": "registry.terraform.io/hashicorp/aws",
            "change": {
                "actions": [
                    "create"
                ],
                "before": null,
                "after": {
                    "allow_major_version_upgrade": null,

                    ...

                    "timeouts": null
                },
                "after_unknown": {
                    "apply_immediately": true,
                    "arn": true,
                    "availability_zones": true,
                    "cluster_identifier_prefix": true,
                    "cluster_members": true,
                    "cluster_resource_id": true,
                    "db_cluster_parameter_group_name": true,
                    "db_subnet_group_name": true,
                    "endpoint": true,
                    "engine_version": true,
                    "hosted_zone_id": true,
                    "id": true,
                    "kms_key_id": true,
                    "port": true,
                    "preferred_backup_window": true,
                    "preferred_maintenance_window": true,
                    "reader_endpoint": true,
                    "restore_to_point_in_time": [],
                    "s3_import": [],
                    "scaling_configuration": [],
                    "storage_encrypted": true,
                    "vpc_security_group_ids": true
                }
            }
        }
    ],
```

----------------------
### Possible [Name](#){: .text-green-200 .fw-700} values

You may use the additional values for [name](#){: .text-green-200 .fw-700} in addition to any Terrafrom resource type:

> ▪ `a resource`, `any resource`, `resources`
> 
> ▪ `an output`, `any output`, `outputs`
> 
> ▪ `a variable`, `any variable`, `variables`
