# CHANGELOG

### 1.0.11 (2019-06-28)
* Added a new step: _its value must/must not be null_ [#106](https://github.com/eerkunt/terraform-compliance/blob/master/example/example_01/aws/restrict_resource_creation.feature) [#105](https://github.com/eerkunt/terraform-compliance/issues/106)


### 1.0.10 (2019-06-27)
* Added a new step : [it_fails](https://github.com/eerkunt/terraform-compliance/blob/master/example/example_01/aws/restrict_resource_creation.feature) [#105](https://github.com/eerkunt/terraform-compliance/issues/105)
 
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
