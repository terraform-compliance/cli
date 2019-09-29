---
layout: default
title: GIVEN Directives
nav_order: 1
has_children: false
parent: BDD Reference
---

# GIVEN

`GIVEN` directive is use to set the initial standard about the type of the entity that you are searching for.

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

or depending on use a [Scenario Outline](/pages/bdd-references#Scenario) instead of a Scenario, it can also 
be a variable like ;

```gherkin
Given I have <resource_type> defined
```

## Reference

----------------------
### <span>&#10003;</span> <span class="d-inline-block p-1 v-align-middle text-xs text-grey-lt-000 bg-green-200">Given</span> I have <span class="d-inline-block p-1 v-align-middle text-xs text-grey-lt-000 bg-yellow-200">name</span> <span class="d-inline-block p-1 v-align-middle text-xs text-grey-lt-000 bg-blue-300">type</span> configured 

#### <span class="d-inline-block p-1 v-align-middle text-grey-lt-000 bg-yellow-200">name</span>: name of the key in terraform. 

Examples ;

* `aws_security_group`
* `aws`

In order to define all resources, you can also use ;

* `a resource`
* `any resource`
* `a`
* `any`
* `anything` 



#### <span class="d-inline-block p-1 v-align-middle text-grey-lt-000 bg-blue-300">type</span>: The type of the key.

If can be one of these ;

* `resource`
* `resources`
* `provider`
* `providers`
* `data`
* `datas`
* `variable`
* `variables`

----------------------

### <span>&#10003;</span> <span class="d-inline-block p-1 v-align-middle text-xs text-grey-lt-000 bg-green-200">Given</span> I have <span class="d-inline-block p-1 v-align-middle text-xs text-grey-lt-000 bg-yellow-200">name</span> defined 

#### <span class="d-inline-block p-1 v-align-middle text-grey-lt-000 bg-yellow-200">name</span>: name of the resource. The name must point to a resource. Can not be provider or anything else.

Examples:

* `aws_security_group`
* `aws_s3_bucket`

