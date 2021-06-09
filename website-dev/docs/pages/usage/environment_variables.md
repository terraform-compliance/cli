---
layout: default
title: Env Variables
nav_order: 2
has_children: false
parent: Usage
---

# Environment Variables

{: .d-inline-block }
1.1.3+
{: .label .label-blue}

`terraform-compliance` allows you to override some internals.

| Variable | Description |
|:--------:|:------------|
| `TFC_ERROR` | This variable will change the `Failure` error that is given by `terraform-compliance` by default. It will not change any functionality other than changing the error message.
