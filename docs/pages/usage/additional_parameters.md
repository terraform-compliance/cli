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

* `--no-ansi`: This will enforce color and emoji compatibility for the terminal. 
* `--wip`: This will enable `terraform-compliance` to expect a failure. If the test pass, then exit code will be `1`, otherwise `0`.
 