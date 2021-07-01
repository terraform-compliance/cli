---
layout: default
title: Installing via pip
nav_order: 1
has_children: false
parent: Installation
---

# Installing via pip

`terraform-compliance` is available as as `pip` package in [PyPi](https://pypi.org/project/terraform-compliance/).

It requires Python 3.x to run properly. Installation is pretty standard like any Python package.

```shell
[~] $ pip install terraform-compliance
```

or for faster parsing support (requires orjson)

```shell
[~] $ pip install terraform-compliance[faster_parsing]
```

in some use cases, you may want to create a new virtual environment to encapsulate `terraform-compliance`
installation in your `venv` directory. In order to do that ;

First install `virtualenv` package, if you don't have ;

```shell
[~] $ pip install virtualenv
```

Then create a new virtual environment ;

```shell
[~] $ virtualenv venv
```

`venv` will be our virtual environment directory. If your system is using Python 2.x by default, you can use 

```shell
[~] $ virtualenv venv --python=/path/to/python3/executable
```

for creating a new Python environment supporting with the same version that you provide via `--python` parameter.

After you created your virtual environment, activate it via ;

```shell
[~] $ . venv/bin/activate
```

and just follow the `terraform-compliance` installation defined in the first step.

