---
layout: default
title: Additional Parameters
nav_order: 1
has_children: false
parent: Usage
---

# Additional Parameters

`terraform-compliance` can directly use `radish` parameters if not collapsing with `terraform-compliance`'s. To see the
full parameter list you can use `radish --help` in order to get a full list.

Some of the useful parameters can be listed as ;

* `--early-exit`: Exits the tests when upon failure instead of completing all tests
* `--no-ansi`: No coloured output, which is useful for some pipelines that doesn't support ANSI Colour Codes.
* `--wip`: In case you are trying to test a `terraform-compliance` test that passes when it fails.
 