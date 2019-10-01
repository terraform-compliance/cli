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

### Then it must contain something
> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
[something](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
is enabled
>
| key | Description | Examples |
|:---:|:----------|:-|
| [something](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} | any property within terraform resoruce/provider/etc | `access_key` `ingress` |
 
------------------------
### [Then](#){: .p-1 .text-red-200} [something](#){: .p-1 .text-grey-dk-100 .bg-yellow-200}  is enabled
This step checks if the property has some value defined in it, except the values are `False`, `{}`, `''` or `None` and `[]`

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
[something](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
is enabled
>
> ▪
[Then](#){: .p-1 .text-red-200} 
[something](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
must be enabled 
>
| key | Description | Examples |
|:---:|:----------|:-|
| [something](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} | can be either a generic property from your terraform configuration or templated ones like below for some resources;<br> `encryption at rest`<br> `encrytion in flight` | `server_side_encryption` `encryption at rest` `encryption in flight` `website` |


`encryption at rest` and `encryption in flight` are templated property types to help you to increase
the readability of your BDD test. Please check [templated entities](/pages/bdd-references/templated_entities) 
section for more information.

------------------------
### [Then](#){: .p-1 .text-red-200}  it must [condition](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} have [proto](#){: .p-1 .text-grey-lt-000 .bg-blue-300} protocol and port [port](#){: .p-1 .text-grey-lt-000 .bg-red-200} for [cidr](#){: .p-1 .text-grey-lt-000 .bg-purple-000}
This step is only valid for `aws_security_group` and `aws_security_group_rule` resources. 

> __Possible sentences :__
>
> ▪
[Then](#){: .p-1 .text-red-200} 
it must 
[condition](#){: .p-1 .text-grey-dk-100 .bg-yellow-200} 
have 
[proto](#){: .p-1 .text-grey-lt-000 .bg-blue-300} 
protocol and port 
[port](#){: .p-1 .text-grey-lt-000 .bg-red-200} 
for 
[cidr](#){: .p-1 .text-grey-lt-000 .bg-purple-000}
>
| key | Description | Examples |
|:---:|:----------|:-|
| [condition](#){: .p-1 .text-grey-lt-000 .bg-yellow-200} | defines the conditional search. | Can only be `only`, `not` |
| [proto](#){: .p-1 .text-grey-lt-000 .bg-blue-300} | defines the network transport protocol | Can only be `tcp` or `udp` |
| [port](#){: .p-1 .text-grey-lt-000 .bg-red-200}  | defines the network port or port range. | `80` `443` `8080-8090` |
| [cidr](#){: .p-1 .text-grey-lt-000 .bg-purple-000} | defines the network ip cidr | `0.0.0.0/0` `192.168.0.0/24` `8.8.8.8/32` |
