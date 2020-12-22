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

NOTE: Some properties will act different than others based on if they are a Terraform default property for a given resource. 

For example, tags is a Terraform default property and so each resource which supports tags, will have the tags property present.
The property may be an empty dictionary which is why in the [Examples about tags](/pages/Examples/tags_related.html), the example 
scenario tests for a null value.

KMS Key Ids, are not a Terraform default property and will not be on the resource by default. 

Supported but non-default properties show up in a different section ('after_unknown') of the plan's json file


----------------------
### Possible [Name](#){: .text-green-200 .fw-700} values

You may use the additional values for [name](#){: .text-green-200 .fw-700} in addition to any Terrafrom resource type:

> ▪ `a resource`, `any resource`, `resources`
> 
> ▪ `an output`, `any output`, `outputs`
> 
> ▪ `a variable`, `any variable`, `variables`
