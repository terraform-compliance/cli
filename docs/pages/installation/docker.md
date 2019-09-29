---
layout: default
title: Installing via Docker
nav_order: 2
has_children: false
parent: Installation
---

# Installing/Using via Docker

Every new release of `terraform-compliance` is stored in [Docker Hub](https://hub.docker.com/r/eerkunt/terraform-compliance/). 

You can either download this docker image directly and try to use it, or instead you can create a shell command 
to do this for you easily.

Here is the function for that ;

```shell
[~] $ function terraform-compliance { docker run --rm -v $(pwd):/target -i -t eerkunt/terraform-compliance "$@"; }
```

Whenever there is a new release or if you want to upgrade it to the latest, you can run ;

```shell
[~] $ docker pull eerkunt/terraform-compliance
```

which will download the latest docker image.
