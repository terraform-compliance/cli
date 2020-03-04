---
layout: default
title: THEN Directives
nav_order: 3
has_children: false
parent: BDD Reference
---

# THEN

`THEN` is used to define the matching criteria. It is the decision making step where the 
Scenario fails or passes. It can also be used for drilling down on a multi-layered resource
property, just like some `WHEN` cases. The main difference would be `THEN` cases would fail
if it the property can not be found while drilling down.

Few examples can be ;

```gherkin
Then it must contain server_side_encryption
```

```gherkin
Then its value must match the "^(dev|test|uat|prod)" regex
```

```gherkin
Then its value must be greater than 20
```

Using `THEN` is optional. You might have some use cases that only a `GIVEN` directive 
could be enough for you for setting the initial definitions.

You can use `AND` with `THEN`.

Depending on use a [Scenario Outline](/pages/bdd-references#Scenario) instead of a Scenario, it can also 
be a variable like ;

```gherkin
Then its value must be <pattern>
```

When a `THEN` step fails to complete, the next steps will not be executed and the scenario
will be deemed to fail. If `terraform-compliance` is used with `--early-exit` parameter then
other scenarios - if exists - won't be executed. This is useful on use cases where you have
lots of tests. 

## Reference
* Table of Contents
{:toc}

### [Then](#){: .p-1 .text-red-200} it must contain [something](#){: .p-1 .text-green-200 .fw-700} 

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
[something](#){: .p-1 .text-green-200 .fw-700} 
is enabled
>
| key | Description | Examples |
|:---:|:----------|:-|
| [something](#){: .p-1 .text-green-200 .fw-700} | any property within terraform resoruce/provider/etc | `access_key` `ingress` |
 
------------------------
### [Then](#){: .p-1 .text-red-200} [something](#){: .p-1 .text-green-200 .fw-700} is enabled
This step checks if the property has some value defined in it, except the values are `False`, `{}`, `''` or `None` and `[]`

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
[something](#){: .p-1 .text-green-200 .fw-700} 
is enabled
>
> ▪
[Then](#){: .p-1 .text-red-200} 
[something](#){: .p-1 .text-green-200 .fw-700} 
must be enabled 
>
| key | Description | Examples |
|:---:|:----------|:-|
| [something](#){: .p-1 .text-green-200 .fw-700} | can be either a generic property from your terraform configuration or templated ones like below for some resources;<br> `encryption at rest`<br> `encrytion in flight` | `server_side_encryption` `encryption at rest` `encryption in flight` `website` |


`encryption at rest` and `encryption in flight` are templated property types to help you to increase
the readability of your BDD test. Please check [templated entities](/pages/bdd-references/templated_entities) 
section for more information.

------------------------
### [Then](#){: .p-1 .text-red-200}  it must [condition](#){: .p-1 .text-green-200 .fw-700} have [proto](#){: .p-1 .text-blue-100 .fw-700} protocol and port [port](#){: .p-1 .text-purple-000 .fw-700} for [cidr](#){: .p-1 .text-yellow-300 .fw-700}
This step is only valid for `aws_security_group` resources. 

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
it  
[condition](#){: .p-1 .text-green-200 .fw-700} 
have 
[proto](#){: .p-1 .text-blue-100 .fw-700} 
protocol and port 
[port](#){: .p-1 .text-purple-000 .fw-700} 
for 
[cidr](#){: .p-1 .text-yellow-300 .fw-700}
>
| key | Description | Examples |
|:---:|:----------|:-|
| [condition](#){: .p-1 .text-green-200 .fw-700} | defines the conditional search. | Can only be `must`, `must not`, `must only` |
| [proto](#){: .p-1 .text-blue-100 .fw-700} | defines the network transport protocol | Can only be `tcp` or `udp` |
| [port](#){: .p-1 .text-purple-000 .fw-700}  | defines the network port, list of ports or a port range. | `80` `443` `8080-8090` `443, 80, 22`|
| [cidr](#){: .p-1 .text-yellow-300 .fw-700} | defines the network ip cidr | `0.0.0.0/0` `192.168.0.0/24` `8.8.8.8/32` |

This step will execute tests that is applicable for both per rule and per security group, depending on the 
[condition](#){: .p-1 .text-green-200 .fw-700} ;

* **must**: The port(s) given must be a subset of the configured ports in related Security Group.
* **must not**: The port(s) given must not exist in ANY rule of the Security Group.
* **must only**: The port(s) given must be exactly same like the ones defined in Security Group.

Please not that `must not` condition is executed per every Security Group Rule, while `must not` and `must only` is 
executed for ALL rules exist in a Security Group.

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
| key | Description | Examples |
|:---:|:----------|:-|
| [property](#){: .p-1 .text-green-200 .fw-700} | any property that resource have (e.g. `name`, `address`, etc. ). Using `address` will give the terraform object name | `address` `name` `size`|
| [something](#){: .p-1 .text-blue-100 .fw-700} | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G`|

------------------------
### [Then](#){: .p-1 .text-red-200} its value must be [action](#){: .p-1 .text-green-200 .fw-700} than [number](#){: .p-1 .text-blue-100 .fw-700} 
This step is for mathematical comparison. It requires to have a [specific `WHEN` directive](/pages/bdd-references/when.html#when-i-action-them) above this line.

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
its value must be 
[action](#){: .p-1 .text-green-200 .fw-700} 
than 
[number](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[Then](#){: .p-1 .text-red-200} 
I expect the result is
[action](#){: .p-1 .text-green-200 .fw-700} 
than 
[number](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[Then](#){: .p-1 .text-red-200} 
its value must be
[action](#){: .p-1 .text-green-200 .fw-700} 
to 
[number](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[Then](#){: .p-1 .text-red-200} 
I expect the result is 
[action](#){: .p-1 .text-green-200 .fw-700} 
to 
[number](#){: .p-1 .text-blue-100 .fw-700} 
>
| key | Description | Examples |
|:---:|:----------|:-|
| [action](#){: .p-1 .text-green-200 .fw-700} | mathematical operator | Only supports for : <br>▪ `more` `greater` `bigger`<br>▪ `more and equal` `greater and equal` `bigger and equal`<br>▪ `less and equal` `lesser and equal` `smaller and equal`<br>▪ `equal`|
| [number](#){: .p-1 .text-blue-100 .fw-700}  | integer | `1` `20` `-40` |

------------------------
### [Then](#){: .p-1 .text-red-200} its value [condition](#){: .p-1 .text-green-200 .fw-700} match the "[search regex](#){: .p-1 .text-blue-100 .fw-700}" regex
This step requires fundamental knowledge about regular expressions due the pattern matching algorithm. It is highly
recommended to check for your patterns in [regex101](https://regex101.com/) before you implement your tests.

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
its value
[condition](#){: .p-1 .text-green-200 .fw-700} 
match the  
"[search_regex](#){: .p-1 .text-blue-100 .fw-700}" 
regex
>
| key | Description | Examples |
|:---:|:----------|:-|
| [condition](#){: .p-1 .text-green-200 .fw-700} | defines positive or negative comparison | Only supports for : <br>▪ Leave it empty for positive comparison<br>▪ Use `must not` for negative comparison |
| [search_regex](#){: .p-1 .text-blue-100 .fw-700}  | any valid regular expression | `^some_name$` `^(you|can|use|or|like|this)$` `\d+` |

__Please note that__, in case you are using a [Scenario Outline instead of a Scenario](/pages/bdd-references/#scenario)
and if you need to use `|` (or) regular expression operator within your [search_regex](#){: .p-1 .text-blue-100 .fw-700} 
regex, then you must use escape characters (`\`) for not to interfere with Scenario Outline structure. In these situations
use `\|` instead of `|`.

------------------------
### [Then](#){: .p-1 .text-red-200} its value [condition](#){: .p-1 .text-green-200 .fw-700} be [something](#){: .p-1 .text-blue-100 .fw-700}
This step is a simplified step for searching something without writing any regular expression. This step will transform
[something](#){: .p-1 .text-blue-100 .fw-700}
into `^something$` and trigger the [Then its value condition match the "search regex" regex"](/pages/bdd-references/then.html#then-its-value-condition-match-the-search-regex-regex)
step.

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
its value
[condition](#){: .p-1 .text-green-200 .fw-700} 
be 
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
| key | Description | Examples |
|:---:|:----------|:-|
| [condition](#){: .p-1 .text-green-200 .fw-700} | defines positive or negative comparison | Only supports for : <br>▪ `must`<br>▪ `must not` |
| [something](#){: .p-1 .text-blue-100 .fw-700}  | search value | `some_name` |

------------------------
### [Then](#){: .p-1 .text-red-200} its value [condition](#){: .p-1 .text-green-200 .fw-700} contain [something](#){: .p-1 .text-blue-100 .fw-700}
Unlike the step supporting regular expression, this step does not support any regular expression.

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
its value
[condition](#){: .p-1 .text-green-200 .fw-700} 
contain 
[something](#){: .p-1 .text-blue-100 .fw-700} 
>
| key | Description | Examples |
|:---:|:----------|:-|
| [condition](#){: .p-1 .text-green-200 .fw-700} | defines positive or negative comparison | Only supports for : <br>▪ `must`<br>▪ `must not` |
| [something](#){: .p-1 .text-blue-100 .fw-700}  | search value | `some_name` |

------------------------
### [Then](#){: .p-1 .text-red-200} its value [condition](#){: .p-1 .text-green-200 .fw-700} be null
This step will checks if filtered value from parent steps is `null`, `` or not assigned any value. 

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
its value
[condition](#){: .p-1 .text-green-200 .fw-700} 
be null
>
| key | Description | Examples |
|:---:|:----------|:-|
| [condition](#){: .p-1 .text-green-200 .fw-700} | defines positive or negative comparison | Only supports for : <br>▪ `must`<br>▪ `must not` |

------------------------
### [Then](#){: .p-1 .text-red-200} it fails
This steps will always makes the scenario fails. Thus, it requires that the test logic is defined on parent steps. If one
of the parent steps declared a `skip` (e.g. [When](/pages/bdd-references/when.html) steps), then all child steps including
this step - if exists in the same scenario - will be skipped and your scenario will pass.

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
it fails
>
> ▪
[Then](#){: .p-1 .text-red-200} 
the scenario fails
>
> ▪
[Then](#){: .p-1 .text-red-200} 
the scenario should fail
>
> ▪
[Then](#){: .p-1 .text-red-200} 
the scenario must fail
>
> ▪
[Then](#){: .p-1 .text-red-200} 
it should fail
>
> ▪
[Then](#){: .p-1 .text-red-200} 
it must fail
>

------------------------
### [Then](#){: .p-1 .text-red-200} it must have [address](#){: .p-1 .text-green-200 .fw-700} referenced
`terraform-compliance` mounts resources into each other if they are referenced. E.g. an `aws_security_group_rule` onto
`aws_security_grouup`. Some use cases may require to find these references, mount points about which entity is mounted 
on top of which entity. This step can be used in these situations.

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
its must have
[address](#){: .p-1 .text-green-200 .fw-700} 
referenced
>

| key | Description | Examples |
|:---:|:----------|:-|
| [address](#){: .p-1 .text-green-200 .fw-700} | resource address within terraform | `aws_security_group.my_group` |

------------------------
### [Then](#){: .p-1 .text-red-200} its [key](#){: .p-1 .text-green-200 .fw-700} [condition](#){: .p-1 .text-blue-100 .fw-700} be [value](#){: .p-1 .text-blue-100 .fw-700} 
This is an optimised way of reading and matching a data without drilling down once more by using `it contains` steps.
This step will match `key` = `value` or `key` != `value` depending on the `condition`

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
its
[key](#){: .p-1 .text-green-200 .fw-700}
[condition](#){: .p-1 .text-blue-100 .fw-700}
be
[value](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[Then](#){: .p-1 .text-red-200} 
its
[key](#){: .p-1 .text-green-200 .fw-700}
property
[condition](#){: .p-1 .text-blue-100 .fw-700}
be
[value](#){: .p-1 .text-blue-100 .fw-700} 
>
> ▪
[Then](#){: .p-1 .text-red-200} 
its
[key](#){: .p-1 .text-green-200 .fw-700}
key
[condition](#){: .p-1 .text-blue-100 .fw-700}
be
[value](#){: .p-1 .text-blue-100 .fw-700} 
>

| key | Description | Examples |
|:---:|:----------|:-|
| [key](#){: .p-1 .text-green-200 .fw-700} | The key name of the property | `encryption`, `private`, `name`, `id` |
| [condition](#){: .p-1 .text-blue-100 .fw-700} | Defines if the match will be `=` or `!=` | Only `must` and `must not` |
| [value](#){: .p-1 .text-blue-100 .fw-700} | The value of the property | `true`, `closed`, `my_bucket` |

------------------------
### [Then](#){: .p-1 .text-red-200} I flatten all values found
This will apply a `union/combine/merge` function for the values that has been found for the resources from the previous
steps. A valid use case could be checking a value that exists in a list of values that has been combined into one. For 
example, checking a specific `name` that has been created by a `for_each` of resource iteration.

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
I flatten all values found
>
