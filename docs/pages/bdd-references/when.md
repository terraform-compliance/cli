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

Using `WHEN` is optional. You might have some use cases that only a `GIVEN` directive could be enough for you.


Depending on use a [Scenario Outline](/pages/bdd-references#Scenario) instead of a Scenario, it can also 
be a variable like ;

```gherkin
When it contains <some_property>
```

## Reference
* Table of Contents
{:toc}

### When it contains something
<span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> it contain <span class="d-inline-block text-small p-1 text-grey-dk-300 bg-yellow-200">something</span> 
<br><span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> it contains <span class="d-inline-block p-1 text-small text-grey-dk-300 bg-yellow-200">something</span>
<br><span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> it must contain <span class="d-inline-block p-1 text-small text-grey-dk-300 bg-yellow-200">something</span>
<br><span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> it has <span class="d-inline-block p-1 text-small text-grey-dk-300 bg-yellow-200">something</span>
<br><span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> they have <span class="d-inline-block p-1 text-small text-grey-dk-300 bg-yellow-200">something</span>

| key | Description | Examples |
|-----|----------|-|
| <center><span class="d-inline-block p-1 text-small text-grey-dk-300 bg-yellow-200">something</span></center> | any property within terraform resoruce/provider/etc | `access_key` `ingress` |

> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-red-300">!!!</span>: _the step, scenario and feature will fail in case that step fails. when __must__ occurs in the step sentence._ 

------------------------
### When its property has something
This is a filtering function. Thus, found resources from previous step will be filtered based on these values.

<span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> its <span class="d-inline-block text-small p-1 text-grey-dk-300 bg-yellow-200">property</span> is <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-blue-300">value</span>
<br><span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> its <span class="d-inline-block text-small p-1 text-grey-dk-300 bg-yellow-200">property</span> has <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-blue-300">value</span>
<br><span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> its <span class="d-inline-block text-small p-1 text-grey-dk-300 bg-yellow-200">property</span> includes <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-blue-300">value</span>
<br><span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> its <span class="d-inline-block text-small p-1 text-grey-dk-300 bg-yellow-200">property</span> consists <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-blue-300">value</span>

| key | Description | Examples |
|-----|-------------|----------|
| <center><span class="d-inline-block p-1 text-small text-grey-dk-300 bg-yellow-200">property</span></center> | any property that resource have (e.g. `name`, `address`, etc. ). Using `address` will give the terraform object name | `address` `name` `size`|
| <center><span class="d-inline-block p-1 text-small text-grey-lt-000 bg-blue-300">something</span> | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G`|

------------------------
### When its property has not something
This is a filtering function. Thus, found resources from previous step will be filtered based on these values.

<span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> its <span class="d-inline-block text-small p-1 text-grey-dk-300 bg-yellow-200">property</span> is not <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-blue-300">value</span>
<br><span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> its <span class="d-inline-block text-small p-1 text-grey-dk-300 bg-yellow-200">property</span> has not <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-blue-300">value</span>
<br><span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> its <span class="d-inline-block text-small p-1 text-grey-dk-300 bg-yellow-200">property</span> does not include <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-blue-300">value</span>
<br><span>&#10003;</span> <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-green-200">When</span> its <span class="d-inline-block text-small p-1 text-grey-dk-300 bg-yellow-200">property</span> does not consist <span class="d-inline-block p-1 text-small text-grey-lt-000 bg-blue-300">value</span>

| key | Description | Examples |
|-----|-------------|----------|
| <center><span class="d-inline-block p-1 text-small text-grey-dk-300 bg-yellow-200">property</span></center> | any property that resource have (e.g. `name`, `address`, etc. ). Using `address` will give the terraform object name | `address` `name` `size`|
| <center><span class="d-inline-block p-1 text-small text-grey-lt-000 bg-blue-300">something</span> | any string or numeric value that the property has. | `s3_my_bucket` `my-bucket` `50G`|
