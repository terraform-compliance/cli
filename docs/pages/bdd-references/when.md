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
`terraform-compliance`. It means the definition criteria (not the testing criteria) defined in your Scenario does
not met with the infrastructure plan.

## Reference
* Table of Contents
{:toc}

### [When](#){: .p-1 .text-red-200} it contains [something](#){: .p-1 .text-green-200 .fw-700}

{: .d-inline-block }
will be deprecated soon
{: .label .label-blue}

This step filters and drills down at the same time, unlike other WHEN steps. Please use [`When it has something`](https://terraform-compliance.com/pages/bdd-references/when.html#when-it-has-something) followed by [`Then it must have something`](https://terraform-compliance.com/pages/bdd-references/then.html#then-it-must-contain-something) to achieve a similar functionality.

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
| key | Description | Examples |
|:---:|:----------|:-|
| [something](#){: .p-1 .text-green-200 .fw-700} | any property within Terraform resource/provider/etc | `access_key` `ingress` `"something with spaces"` |

### [When](#){: .p-1 .text-red-200} it has [something](#){: .p-1 .text-green-200 .fw-700}

{: .d-inline-block }
1.2.+
{: .label .label-blue}

This is a filtering function where the resources from previous step will be filtered based on the "something" key exist
in the resource properties.

> __Possible sentences :__
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
| [something](#){: .p-1 .text-green-200 .fw-700} | any property within Terraform resource/provider/etc | `access_key` `ingress` `"something with spaces"` |

### [When](#){: .p-1 .text-red-200} it does not have [something](#){: .p-1 .text-green-200 .fw-700}

{: .d-inline-block }
1.2.+
{: .label .label-blue}

This is a filtering function where the resources from previous step will be filtered based on the "something" key not existing
in the resource properties.

> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200}
it does not contain
[something](#){: .p-1 .text-green-200 .fw-700}
>
> ▪
[When](#){: .p-1 .text-red-200}
it doesnt contain
[something](#){: .p-1 .text-green-200 .fw-700}
>
> ▪
[When](#){: .p-1 .text-red-200}
it does not have
[something](#){: .p-1 .text-green-200 .fw-700}
>
> ▪
[When](#){: .p-1 .text-red-200}
it doesnt have
[something](#){: .p-1 .text-green-200 .fw-700}
>
> ▪
[When](#){: .p-1 .text-red-200}
they do not have
[something](#){: .p-1 .text-green-200 .fw-700}
>
> ▪
[When](#){: .p-1 .text-red-200}
they dont have
[something](#){: .p-1 .text-green-200 .fw-700}
>
| key | Description | Examples |
|:---:|:----------|:-|
| [something](#){: .p-1 .text-green-200 .fw-700} | any property within Terraform source/provider/etc | `access_key` `ingress` `"something with spaces"` |


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
contains
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
contains
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700}
"
>
> ▪
[When](#){: .p-1 .text-red-200}
its
[dictionary](#){: .p-1 .text-green-200 .fw-700}
includes an entry where
"
[key](#){: .p-1 .text-blue-100 .fw-700}
"
is
"
[value](#){: .p-1 .text-blue-100 .fw-700}
"
>
>
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-green-200 .fw-700} | any property that resources have. Using `type` will give the Terraform resource type; `address` is the name you have given it | `address` `name` `size` |
| [dictionary](#){: .p-1 .text-green-200 .fw-700} | a dictionary property that resource has. | `tags` |
| [something](#){: .p-1 .text-blue-100 .fw-700} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G` `"something with spaces"` |
| [some string with spaces](#){: .p-1 .text-blue-100 .fw-700} | any string (allows spaces). | `my dictionary key` |
| [key](#){: .p-1 .text-blue-100 .fw-700} | any dictionary key (allows spaces). | `my dictionary key` |
| [value](#){: .p-1 .text-blue-100 .fw-700} | any dictionary value (allows spaces). | `my dictionary value` |

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
does not contain
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
does not contain
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700}
"
>
> ▪
[When](#){: .p-1 .text-red-200}
its
[dictionary](#){: .p-1 .text-green-200 .fw-700}
does not include an entry where
"
[key](#){: .p-1 .text-blue-100 .fw-700}
"
is
"
[value](#){: .p-1 .text-blue-100 .fw-700}
"
>
>
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-green-200 .fw-700} | any property that resources have. Using `type` will give the Terraform resource type; `address` is the name you have given it | `address` `name` `size`|
| [dictionary](#){: .p-1 .text-green-200 .fw-700} | a dictionary property that resource has. | `tags` |
| [something](#){: .p-1 .text-blue-100 .fw-700} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G` `"something with spaces"` |
| [some string with spaces](#){: .p-1 .text-blue-100 .fw-700} | any string (allows spaces). | `my dictionary key` |
| [key](#){: .p-1 .text-blue-100 .fw-700} | any dictionary key (allows spaces). | `my dictionary key` |
| [value](#){: .p-1 .text-blue-100 .fw-700} | any dictionary value (allows spaces). | `my dictionary value` |

------------------------
### [When](#){: .p-1 .text-red-200} its [property](#){: .p-1 .text-green-200 .fw-700} metadata has [something](#){: .p-1 .text-blue-100 .fw-700}
This is a filtering function. Thus, found resources from previous step will be filtered based on these values.

This step checks if a property metadata has a specific value. Metadata are considered to be key, value pairs outside of `values`, which includes the properties of the resource.

Following is how an `aws_instance` example is represented in stash.
```
{'address': 'aws_instance.example',
 'mode': 'managed',
 'type': 'aws_instance',
 'name': 'example',
 'provider_name': 'registry.terraform.io/hashicorp/aws',
 'values': {
  'ami': 'ami-034bf895b736be04a',
  'arn': 'arn:aws:ec2:us-west-1:704778554736:instance/i-0d6a689453a806e50',
  'tags': {'Name': 'HelloWorldChange'},
  ...
  },
 'actions': ['update']
}
```
`actions`, `provider_name`, or `address` are considered to be metadata. However `ami`, `arn`, and `tags` are considered to be otherwise, as they are in `values`. The [debugger](https://terraform-compliance.com/pages/usage/#-d--debug) could be used to see the metadata present at a given step.

> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200}
its
[property](#){: .p-1 .text-green-200 .fw-700}
metadata is
[something](#){: .p-1 .text-blue-100 .fw-700}
>
> ▪
[When](#){: .p-1 .text-red-200}
its
[property](#){: .p-1 .text-green-200 .fw-700}
metadata has
[something](#){: .p-1 .text-blue-100 .fw-700}
>
> ▪
[When](#){: .p-1 .text-red-200}
its
[property](#){: .p-1 .text-green-200 .fw-700}
metadata includes
[something](#){: .p-1 .text-blue-100 .fw-700}
>
> ▪
[When](#){: .p-1 .text-red-200}
its
[property](#){: .p-1 .text-green-200 .fw-700}
metadata contains
[something](#){: .p-1 .text-blue-100 .fw-700}
>
>
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-green-200 .fw-700} | any metadata that resources have. Using `actions` will give the Terraform's actions on the resource on an apply; `address` is the name you have given it | `address` `name` `actions` |
| [something](#){: .p-1 .text-blue-100 .fw-700} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `create` `"something with spaces"` |

------------------------
### [When](#){: .p-1 .text-red-200} its [property](#){: .p-1 .text-green-200 .fw-700} metadata has not [something](#){: .p-1 .text-blue-100 .fw-700}
This is a filtering function. Thus, found resources from previous step will be filtered based on these values.

This step filters a resource out if it has `property` metadata that has `something` value. Metadata are considered to be key, value pairs outside of `values`, which includes the properties of the resource.

Following is how an `aws_instance` example is represented in stash.
```
{'address': 'aws_instance.example',
 'mode': 'managed',
 'type': 'aws_instance',
 'name': 'example',
 'provider_name': 'registry.terraform.io/hashicorp/aws',
 'values': {
  'ami': 'ami-034bf895b736be04a',
  'arn': 'arn:aws:ec2:us-west-1:704778554736:instance/i-0d6a689453a806e50',
  'tags': {'Name': 'HelloWorldChange'},
  ...
  },
 'actions': ['update']
}
```
`actions`, `provider_name`, or `address` are considered to be metadata. However `ami`, `arn`, and `tags` are considered to be otherwise, as they are in `values`. The [debugger](https://terraform-compliance.com/pages/usage/#-d--debug) could be used to see the metadata present at a given step.

> __Possible sentences :__
>
> ▪
[When](#){: .p-1 .text-red-200}
its
[property](#){: .p-1 .text-green-200 .fw-700}
metadata is not
[something](#){: .p-1 .text-blue-100 .fw-700}
>
> ▪
[When](#){: .p-1 .text-red-200}
its
[property](#){: .p-1 .text-green-200 .fw-700}
metadata has not
[something](#){: .p-1 .text-blue-100 .fw-700}
>
> ▪
[When](#){: .p-1 .text-red-200}
its
[property](#){: .p-1 .text-green-200 .fw-700}
metadata does not have
[something](#){: .p-1 .text-blue-100 .fw-700}
>
> ▪
[When](#){: .p-1 .text-red-200}
its
[property](#){: .p-1 .text-green-200 .fw-700}
metadata does not include
[something](#){: .p-1 .text-blue-100 .fw-700}
>
> ▪
[When](#){: .p-1 .text-red-200}
its
[property](#){: .p-1 .text-green-200 .fw-700}
metadata does not contain
[something](#){: .p-1 .text-blue-100 .fw-700}
>
>
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-green-200 .fw-700} | any metadata that resources have. Using `actions` will give the Terraform's actions on the resource on an apply; `address` is the name you have given it | `address` `name` `actions` |
| [something](#){: .p-1 .text-blue-100 .fw-700} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `create` `"something with spaces"` |

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
reference contains
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
reference contains
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700}
"
>
>
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-green-200 .fw-700} | any property that is used for referencing another resource.  | `security_group_id` `aws_instance` `"something with spaces"` |
| [something](#){: .p-1 .text-blue-100 .fw-700} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G` `"something with spaces"` |
| [some string with spaces](#){: .p-1 .text-blue-100 .fw-700} | any string (allows spaces). | `my dictionary key` |

------------------------
### [When](#){: .p-1 .text-red-200} its [property](#){: .p-1 .text-green-200 .fw-700} reference has not [something](#){: .p-1 .text-blue-100 .fw-700}
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
reference does not contain
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
reference does not contain
"
[some string with spaces](#){: .p-1 .text-blue-100 .fw-700}
"
>
>
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-green-200 .fw-700} | any property that is used for referencing another resource.  | `security_group_id` `aws_instance` `"something with spaces"` |
| [something](#){: .p-1 .text-blue-100 .fw-700} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G` `"something with spaces"` |
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
