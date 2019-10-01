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

Few examples can be ;

```gherkin
Given I have AWS S3 Bucket defined
```

```gherkin
Given I have aws provider configured
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

### [Given](#){: .p-1 .text-red-200} I have [name](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} [type](#){: .p-1 .text-grey-lt-000 .bg-blue-300} configured


> __Possible sentences :__
>
> ▪
[Given](#){: .p-1 .text-red-200} 
I have 
[name](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
[type](#){: .p-1 .text-grey-lt-000 .bg-blue-300} 
configured
>
| key | Description | Examples |
|:---:|:----------|:-|
| [name](#){: .p-1 .text-grey-dk-100 .bg-yellow-200}  | name of the key in terraform. | `aws_security_group` `ingress`<br><br>In order to define all resources, you can also use ;<br><br>`a resource` `any resource` `a` `any` `anything` |
| [type](#){: .p-1 .text-grey-lt-000 .bg-blue-300}  | The type of the key. | It can be one of these ;<br>`resource` `resources` `provider` `providers` `data` `datas` `variable` `variables` |

----------------------
### [Given](#){: .p-1 .text-red-200} I have [name](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} defined


> __Possible sentences :__
>
> ▪
[Given](#){: .p-1 .text-red-200} 
I have 
[name](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
defined
>
| key | Description | Examples |
|:---:|:----------|:-|
| [name](#){: .p-1 .text-grey-dk-100 .bg-yellow-200}  | name of the resource. The name must point to a resource. Can not be `provider` or anything else. | `aws_security_group` `aws_s3_bucket` |

