---
layout: default
title: WHEN Directives
nav_order: 2
has_children: false
parent: BDD Reference
---

# WHEN

`WHEN` used to define the condition that you are searching for. It could be either a filtering condition or you might be
looking for a specific property on a resource, or any property on any entity that has been transferred via [GIVEN](/pages/bdd-references/given)
directive. `WHEN` must come after `GIVEN` directive.

`WHEN` steps does not fail any scenario. It sets the condition for the further steps.

`WHEN` can be used multiple times, either with using `WHEN` or `AND`

Few examples can be ;

```gherkin
When I count them
```

```gherkin
When its name is my-bucket
```

```gherkin
When it contains server_side_encryption
```

Using `WHEN` is optional. You might have some use cases that only a `GIVEN` and some `THEN`
directives could be enough for you.

You can use `AND` with `WHEN`.

Depending on use a [Scenario Outline](/pages/bdd-references#Scenario) instead of a Scenario, it can also 
be a variable like ;

```gherkin
When it contains <some_property>
```

In case a `WHEN` step fails to complete, then the step and further steps will be `SKIPPED`. Skipped steps won't fail
`terraform-compliance`. It means the definition criterias (not the testing criterias) defined in your Scenario does 
not met with the infrastructure plan.

## Reference
* Table of Contents
{:toc}

### [When](#){: .p-1 .text-red-200} it contains [something](#){: .p-1 .text-green-200 .fw-700}


> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200} 
it contain
[something](#){: .p-1 .text-green-200 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
it contains
[something](#){: .p-1 .text-green-200 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
it has
[something](#){: .p-1 .text-green-200 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
they have
[something](#){: .p-1 .text-green-200 .fw-700} 
>
| key | Description | Examples |
|:---:|:----------|:-|
| [something](#){: .p-1 .text-green-200 .fw-700} | any property within terraform resoruce/provider/etc | `access_key` `ingress` |
 
 
------------------------
### [When](#){: .p-1 .text-red-200} its [property](#){: .p-1 .text-green-200 .fw-700} has [something](#){: .p-1 .text-blue-100 .fw-700}
This is a filtering function. Thus, found resources from previous step will be filtered based on these values.

> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
is
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
has
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
includes
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
consists
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
is
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
has
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
includes
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
consists
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
>
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-green-200 .fw-700} | any property that resource have (e.g. `name`, `address`, etc. ). Using `address` will give the terraform object name | `address` `name` `size` |
| [something](#){: .p-1 .text-blue-100 .fw-700} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G` |
| [some string with spaces](#){: .p-1 .text-blue-100 .fw-700} | any string (allows spaces). | `my dictionary key` |

------------------------
### [When](#){: .p-1 .text-red-200} its [property](#){: .p-1 .text-green-200 .fw-700} reference has [something](#){: .p-1 .text-blue-100 .fw-700}
This is a filtering function, specific for resource referencing. The resource references will be checked based on
the `property` property defined within the step.

> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference is
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference has
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference includes
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference consists
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference is
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference has
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference includes
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference consists
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
>
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-green-200 .fw-700} | any property that is used for referencing another resource.  | `security_group_id` `aws_instance` |
| [something](#){: .p-1 .text-blue-100 .fw-700} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G` |
| [some string with spaces](#){: .p-1 .text-blue-100 .fw-700} | any string (allows spaces). | `my dictionary key` |

------------------------
### [When](#){: .p-1 .text-red-200} its [property](#){: .p-1 .text-green-200 .fw-700} has not [something](#){: .p-1 .text-blue-100 .fw-700}
This is a filtering function. Thus, found resources from previous step will be filtered based on these values.

> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
is not
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
has not 
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
does not include
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
does not consist
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
is not
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
has not 
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
does not include
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
does not consist
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
>
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-green-200 .fw-700} | any property that resource have (e.g. `name`, `address`, etc. ). Using `address` will give the terraform object name | `address` `name` `size`|
| [something](#){: .p-1 .text-blue-100 .fw-700} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G`|
| [some string with spaces](#){: .p-1 .text-blue-100 .fw-700} | any string (allows spaces). | `my dictionary key` |

------------------------
### [When](#){: .p-1 .text-red-200} its [property](#){: .p-1 .text-green-200 .fw-700} reference has [something](#){: .p-1 .text-blue-100 .fw-700}
This is a filtering function, specific for resource referencing. The resource references will be checked based on
the `property` property defined within the step. This is the negative version (ref. `not` usage within the step) of the
filtering step.

> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference is not
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference has not
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference does not include
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference does not consist
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference is not
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference has not
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference does not include
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-green-200 .fw-700} 
reference does not consist
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700} 
"
>
>
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-green-200 .fw-700} | any property that is used for referencing another resource.  | `security_group_id` `aws_instance` |
| [something](#){: .p-1 .text-blue-100 .fw-700} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G` |
| [some string with spaces](#){: .p-1 .text-blue-100 .fw-700} | any string (allows spaces). | `my dictionary key` |


------------------------
### [When](#){: .p-1 .text-red-200} I [action](#){: .p-1 .text-green-200 .fw-700} them
This step is for mathematical operations. Currently it is only supported for `count`

> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200} 
I
[action](#){: .p-1 .text-green-200 .fw-700} 
them
>
> ▪
[When](#){: .p-1 .text-red-200} 
I
[action](#){: .p-1 .text-green-200 .fw-700} 
it
>
> ▪
[When](#){: .p-1 .text-red-200} 
I
[action](#){: .p-1 .text-green-200 .fw-700} 
the value
>
| key | Description | Examples |
|:---:|:----------|:-|
| [action](#){: .p-1 .text-green-200 .fw-700} | mathematical operation | currently only supports for `count` |
