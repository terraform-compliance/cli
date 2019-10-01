---
layout: default
title: Templated Entities
nav_order: 5
has_children: false
parent: BDD Reference
---

# Templated Entities

`terraform-compliance` supports native resource type referencing that can be used as same in your tests and terraform 
code.

For example a test against this terraform code ;

```
resource "aws_s3_bucket" "my-bucket" {
  bucket = "some-bucket-name"
  acl    = "private"

  ...
}
```

can be written as ;

```gherkin
Feature: My test feature

Scenario: Ensure my specific s3 buckets are private
  Given I have aws_s3_bucket defined
  Then it must contain acl
  And its value must be private
```

While this is quite easy to understand, you can also write the same test as ;

```gherkin
Feature: My test feature

Scenario: Ensure my specific s3 buckets are private
  Given I have AWS S3 Bucket defined
  Then it must contain acl
  And its value must be private
```

where we used ;

```gherkin
  Given I have AWS S3 Bucket defined
```

instead of ;

```gherkin
  Given I have aws_s3_bucket defined
```

There are few templated entities defined for making the tests more readable. Some about resource types, some about properties
of resources.

Complete list can be found on [github repository](https://github.com/eerkunt/terraform-compliance/blob/master/terraform_compliance/steps/__init__.py)