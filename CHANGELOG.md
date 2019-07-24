# CHANGELOG

### 1.0.29 (2019-07-24)
* Fixed a problem where some `Null/None` values can not be parsed by regex steps. ([#132](https://github.com/eerkunt/terraform-compliance/issues/132)) 

### 1.0.28 (2019-07-23)
* Upgraded `terraform` executable within the docker file from `0.12.3` to `0.12.5`

### 1.0.27 (2019-07-23)
* `its value must not be null` step is also checking for string `null`.
* terraform version checks are more dynamic.
* Fixed some of the examples.

### 1.0.26 (2019-07-23)
* Fixed some of the examples.

### 1.0.25 (2019-07-16)
* Changed `encryption is enabled` step to `{property} is enabled` where `{property}` could be generic and templated. ([#123](https://github.com/eerkunt/terraform-compliance/issues/123))

### 1.0.24 (2019-07-16)
* Fixed a failure message where it was misleading. (follow up on [#127](https://github.com/eerkunt/terraform-compliance/issues/127#issuecomment-511990432)) 
 
### 1.0.23 (2019-07-16)
* Fixed a bug where a resource might have multiple values (with same key). (follow up on [#126](https://github.com/eerkunt/terraform-compliance/issues/126))
* Improved `its value must not be null` step that is also checking if the value is set to `''`.

### 1.0.22 (2019-07-16)
* Fixed a bug where terraform-compliance crashes while reading the terraform file on terraform resources that does not have `values` key ([#124](https://github.com/eerkunt/terraform-compliance/issues/124))
* Fixed a bug where some resources with key/value pair property causes a problem as reported in ([#127](https://github.com/eerkunt/terraform-compliance/issues/127))

### 1.0.21 (2019-07-12)
* Fixed a bug where 'it must contain <something>' fails because of a KeyError.
* Fixed a bug where a test might fail while changing a resource that already exists in the remote/local terraform state.

### 1.0.20 (2019-07-10)
* Set static versions fo dependencies within the setup.py and disabled re-install function completely.

### 1.0.19 (2019-07-08)
* Added filtering capability that will help to filter any resource type by a specific property. ([#122](https://github.com/eerkunt/terraform-compliance/issues/122))

### 1.0.18 (2019-07-08)
* Fixed a problem where searched key exists with a different purpose in the root and some of the child elements. E.g. `tags` in aws_s3_bucket and `tags` in `lifecycle_rules` within that bucket.

### 1.0.17 (2019-07-06)
* Fixed a problem where test are passing directly if one of the drilled down values is a list. ([#121](https://github.com/eerkunt/terraform-compliance/issues/121))
* Improved `I expect the result is {operator} than {number}/Its value must be {operator} than {number}` step where the values can also be read and compared mathematically. ([#120](https://github.com/eerkunt/terraform-compliance/issues/120))

### 1.0.16 (2019-07-02)
* Fixed a problem where terraform values including []/None/False was failing due to being negative.

### 1.0.15 (2019-07-01)
* Fixed a problem where some of the data resources defined in configuration section was not distinguished.

### 1.0.14 (2019-07-01)
* Fixed a problem where 'its value must not be null' was not working properly

### 1.0.13 (2019-06-28)
* Upgraded `radish-bdd` to `0.13.1` which includes fix for using escaped PIPE (`|`) characters within the features. ([Example](https://github.com/eerkunt/terraform-compliance/blob/master/example/example_01/aws/tags.feature)) ([#110](https://github.com/eerkunt/terraform-compliance/issues/110))

### 1.0.12 (2019-06-28)
* Include the Terraform binary in the Docker container for use on non-Linux host operating systems ([#102](https://github.com/eerkunt/terraform-compliance/issues/102))

### 1.0.11 (2019-06-28)
* Added a new step: _its value must/must not be null_ ([Example](https://github.com/eerkunt/terraform-compliance/blob/master/example/example_01/aws/restrict_resource_creation.feature)) ([#106](https://github.com/eerkunt/terraform-compliance/issues/106)))
* Added support for `data` definitions. ([#105](https://github.com/eerkunt/terraform-compliance/issues/111))

### 1.0.10 (2019-06-27)
* Added a new step : [it_fails](https://github.com/eerkunt/terraform-compliance/blob/master/example/example_01/aws/restrict_resource_creation.feature) ([#105](https://github.com/eerkunt/terraform-compliance/issues/105))
 
### 1.0.9 (2019-06-27)
* Improved `contains` steps where in some cases 'key' and 'value' dict keys exist, instead of value of key as a key.

### 1.0.8 (2019-06-26)
* Fixed a problem where mounted resources creating problem on identifying resources that doesn't have `tags` capability. ([#107](https://github.com/eerkunt/terraform-compliance/issues/107))

### 1.0.7 (2019-06-25)
* Tested and added support for `terraform` 0.12.2 and 0.12.3

### 1.0.6 (2019-06-25)
* Improved 'contains' and 'regex' matching steps.

### 1.0.5 (2019-06-24)
* Added basic heredoc support for json strings. ([#90](https://github.com/eerkunt/terraform-compliance/issues/90))
* Added encryption property for (at rest) aws_emr_security_configuration

### 1.0.4 (2019-06-23)
* Added exception handlings for terraform executable and converting plan. ([#99](https://github.com/eerkunt/terraform-compliance/issues/99))

### 1.0.3 (2019-06-23)
* Added S3 Public Block Access example to examples ([#71](https://github.com/eerkunt/terraform-compliance/issues/71))

### 1.0.2 (2019-06-22)
* Fixed an issue where terraform executable does not exist in PATH env variable. ([#99](https://github.com/eerkunt/terraform-compliance/issues/99))
* Added "-t" argument for passing terraform executable if one doesn't want to keep it in PATH env variable.

### 1.0.1 (2019-06-21)
* Fixed an issue where `filetype` module could not be found. ([#97](https://github.com/eerkunt/terraform-compliance/issues/97))
* Upgraded python in Docker image from 3.6.8 to 3.7.3

# 1.0.0 (2019-06-20)
**_BREAKING BACKWARD COMPATIBILITY_** for `terraform-compliance` since the parameters has changed. This is a MAJOR upgrade and a re-design of the tool.
* This version only supports `terraform` 0.12.0 and 0.12.1.
* Removed `-t` parameter.
* Introduced `-p` parameter where `-p` is either ;
	* `terraform plan -out=<file>.out` output file *or*
	* `terraform show -json <file.out> > file.json` output for checking the plan (changes)
	* `terraform show -json` output for checking the whole state
* Instead of parsing `HCL`, `terraform-compliance` is **now** parsing/processing against `terraform show` output.
* Conversion from `terraform` internal plan format to json.
* Full support for `terraform` interpolations and modules.
* Minor upgrades on dependencies
* Removed many methods/functions that was doing `terraform` 's job
* Revamped all steps and required helper functions/methods
* Instead of having `untaggable_resources` now `terraform-compliance` auto-detects if a resource has `tag` property.
* Removed `terraform-validate` usage.
* Introduced internal `terraform-compliance` exceptions instead of generic ones.
* Started to keep a CHANGELOG for better understanding about what happens in the tool :)
