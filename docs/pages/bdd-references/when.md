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

### [When](#){: .p-1 .text-red-200} it contains [something](#){: .p-1 .text-grey-dk-100 .bg-yellow-200}


> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200} 
it contain
[something](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
it contains
[something](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
it has
[something](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
they have
[something](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
>
| key | Description | Examples |
|:---:|:----------|:-|
| [something](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} | any property within terraform resoruce/provider/etc | `access_key` `ingress` |
 
 
------------------------
### [When](#){: .p-1 .text-red-200} its [property](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} has [something](#){: .p-1 .text-grey-lt-000 .bg-blue-300}
This is a filtering function. Thus, found resources from previous step will be filtered based on these values.

> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
is
[something](#){: .p-1 .text-grey-lt-000 .bg-blue-300} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
has
[something](#){: .p-1 .text-grey-lt-000 .bg-blue-300} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
includes
[something](#){: .p-1 .text-grey-lt-000 .bg-blue-300} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
consists
[something](#){: .p-1 .text-grey-lt-000 .bg-blue-300} 
>
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} | any property that resource have (e.g. `name`, `address`, etc. ). Using `address` will give the terraform object name | `address` `name` `size` |
| [something](#){: .p-1 .text-grey-lt-000 .bg-blue-300} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G` |

------------------------
### [When](#){: .p-1 .text-red-200} its [property](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} has not [something](#){: .p-1 .text-grey-lt-000 .bg-blue-300}
This is a filtering function. Thus, found resources from previous step will be filtered based on these values.

> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
is not
[something](#){: .p-1 .text-grey-lt-000 .bg-blue-300} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
has not 
[something](#){: .p-1 .text-grey-lt-000 .bg-blue-300} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
does not include
[something](#){: .p-1 .text-grey-lt-000 .bg-blue-300} 
>
> ▪
[When](#){: .p-1 .text-red-200} 
its 
[property](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
does not consist
[something](#){: .p-1 .text-grey-lt-000 .bg-blue-300} 
>
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} | any property that resource have (e.g. `name`, `address`, etc. ). Using `address` will give the terraform object name | `address` `name` `size`|
| [something](#){: .p-1 .text-grey-lt-000 .bg-blue-300} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G`|

------------------------
### [When](#){: .p-1 .text-red-200} I [action](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} them
This step is for mathematical operations. Currently it is only supported for `count`

> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200} 
I
[action](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
them
>
> ▪
[When](#){: .p-1 .text-red-200} 
I
[action](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
it
>
> ▪
[When](#){: .p-1 .text-red-200} 
I
[action](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
the value
>
| key | Description | Examples |
|:---:|:----------|:-|
| [action](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} | mathematical operation | currently only supports for `count` |

