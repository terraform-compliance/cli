# CHANGELOG

## 1.0.0 (2019-06-20)
**_BREAKING BACKWARD COMPATIBILITY_** for `terraform-compliance` since the parameters has changed. This is a MAJOR upgrade and a re-design of the tool.
* This version only supports `terraform` 0.12.0 and 0.12.1.
* Removed `-t` parameter.
* Introduced `-p` parameter where `-p` is either ;
	* `terraform plan -out=<file>.out` output file *or*
	* `terraform show -json <file.out> > file.json` output for checking the plan (changes)
	* `terraform show -json` output for checking the whole state
* Instead of parsing `HCL`, `terraform-compliance` is not parsing/processing against `terraform show` output.
* Conversion from `terraform` internal plan format to json.
* Full support for `terraform` interpolations and modules.
* Minor upgrades on dependencies
* Removed many methods/functions that was doing `terraform` 's job
* Revamped all steps and required helper functions/methods
* Instead of having `untaggable_resources` now `terraform-compliance` auto-detects if a resource has `tag` property.
* Removed `terraform-validate` usage.
* Introduced internal `terraform-compliance` exceptions instead of generic ones.
* Started to keep a CHANGELOG for better understanding about what happens in the tool :)
