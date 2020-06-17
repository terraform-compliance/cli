# CHANGELOG

## Unreleased
* Fixed faulty over restriction in [Then its singular value condition match the "search_regex" regex](https://terraform-compliance.com/pages/bdd-references/then.html#then-its-singular-value-condition-match-the-search-regex-regex).
- its_key_condition_be_value now abides the two rules: drills down to the value and fails if any resource fails. This could introduce slight backwards incompatibility, but in essence this is a bugfix and not a change.
- Note: (don't put this line into the release) Release with @noskip.

## 1.2.6 (2020-06-12)
* Fixed a bug where failures would break --junit-xml dump. ([#271](https://github.com/eerkunt/terraform-compliance/issues/271))
* Fixed a bug where searching some haystacks would raise an error in seek_value_in_dict. ([#285](https://github.com/eerkunt/terraform-compliance/issues/285))
* New step: [Then all of its values condition match the "search_regex" regex](https://terraform-compliance.com/pages/bdd-references/then.html#then-its-value-condition-match-the-search-regex-regex). ([#285](https://github.com/eerkunt/terraform-compliance/issues/285), [#293](https://github.com/eerkunt/terraform-compliance/issues/293))
* New step: [Then any of its values condition match the "search_regex" regex](https://terraform-compliance.com/pages/bdd-references/then.html#then-any-of-its-values-condition-match-the-search-regex-regex). ([#285](https://github.com/eerkunt/terraform-compliance/issues/285), [#293](https://github.com/eerkunt/terraform-compliance/issues/293))
* New step: [Then its singular value condition match the "search_regex" regex](https://terraform-compliance.com/pages/bdd-references/then.html#then-its-singular-value-condition-match-the-search-regex-regex). ([#285](https://github.com/eerkunt/terraform-compliance/issues/285), [#293](https://github.com/eerkunt/terraform-compliance/issues/293))

## 1.2.5 (2020-06-07)
* Fixed a bug where some empty found values would be treated as not found. ([#249](https://github.com/eerkunt/terraform-compliance/issues/249))
* Improved some error messages that might create some confusion about the failure results. ([#284](https://github.com/eerkunt/terraform-compliance/issues/284))
* Fixed a problem where using `@warning` tag was causing a problem where error messages was hidden on `-q` usage.
* Fixed `@warning` tag where further steps were also executed on a failure condition unintentionally. ([#279](https://github.com/eerkunt/terraform-compliance/issues/279))

## 1.2.4 (2020-06-03)
* Add ability to reference a git repo by branch name and directory via `<repo>.git//<directory>?ref=<branch-name`. ([#218](https://github.com/eerkunt/terraform-compliance/issues/218))

## 1.2.3 (2020-05-25)
* Fixed a crash where some module outputs could not be processed. ([#275](https://github.com/eerkunt/terraform-compliance/issues/275))

## 1.2.2 (2020-05-24)
* Improved resource mounting where some terraform providers were creating inconsistent plan output and omitted some parameters that are referenced to a dynamic resource. ([#260](https://github.com/eerkunt/terraform-compliance/issues/260))
* Fixed an issue where regular expression usage on CIDR steps was causing a problem. ([#265](https://github.com/eerkunt/terraform-compliance/issues/265))

## 1.2.1 (2020-05-19)
* Fixed a problem where properties having a space character were not recognised.
* Optimised key/value (property) definitions on all steps, where all keys or values can also have space characters encapsulated within "". ([#270](https://github.com/eerkunt/terraform-compliance/issues/270))
* Introduced case insensitive matching for the regex steps. ([#268](https://github.com/eerkunt/terraform-compliance/issues/268))

## 1.2.0 (2020-05-12)
* Major code refactoring on the steps for the readability.
* Handled related radish-bdd exceptions and giving out `terraform-compliance` related error information.
* __BREAKING CHANGE :__ Changed `When it has <something>` step sentence where it now works as a true filtering function, unlike `When it contains <something`.
* `When it contains <something>` step still works same with a _Warning_. This step will be deprecated (and converted to `When it has <something>`) in future versions.
* New step: [When it must not have something](https://terraform-compliance.com/pages/bdd-references/when.html#when-it-must-not-have-something). ([#202](https://github.com/eerkunt/terraform-compliance/issues/202))
* New step: [Then it must not have something](https://terraform-compliance.com/pages/bdd-references/then.html#then-it-must-not-have-something). ([#202](https://github.com/eerkunt/terraform-compliance/issues/202))

## 1.1.17 (2020-04-30)
* Fixed a problem where resources/providers starting with `data` was misinterpreted. ([#257](https://github.com/eerkunt/terraform-compliance/issues/257))

## 1.1.16 (2020-04-13)
* Enabled resource mounting/referencing for resources within modules. ([#227](https://github.com/eerkunt/terraform-compliance/issues/227))
* Fixed a problem where `its value must/must not be null` step was not processed properly. ([#247](https://github.com/eerkunt/terraform-compliance/issues/247))
* Fixed a problem where filtering steps was failed with SKIPPING due to different types (or due to type conversions) are compared. ([#248](https://github.com/eerkunt/terraform-compliance/issues/248))
* Enabled Security Group related step for Security Group Rules also, it was only supporting Security Group before.
* Improved Security group processing where a regular expression can also be used while defining CIDRs. ([#216](https://github.com/eerkunt/terraform-compliance/issues/216))
* Improved `resource that support tags` in functionality in `GIVEN` steps where `tags` can be any property. ([#252](https://github.com/eerkunt/terraform-compliance/issues/252))

## 1.1.15 (2020-03-31)
* Improved `resource that support tags` resource type where Auto-Scaling Group style tags are enabled to be processed. ([#243](https://github.com/eerkunt/terraform-compliance/issues/243))
* Improved `When its <key> is <value>` steps for testing a dictionary property key and value like `When its tags includes an entry where "some key" is "some value"`. ([#228](https://github.com/eerkunt/terraform-compliance/issues/228))
* Improved `When its <key> is not <value>` steps for for testing a dictionary property key and value like `When its tags does not include an entry where "some key" is "some value"`. ([#228](https://github.com/eerkunt/terraform-compliance/issues/228))

## 1.1.14 (2020-03-30)
* Fixed a problem where `count` step was counting incorrectly and counting characters of strings, integers and bools. (([#242](https://github.com/eerkunt/terraform-compliance/issues/242))

## 1.1.13 (2020-03-30)
* Fixed a problem where `integer` and `boolean` values where causing comparison problems on `When its <key> contains <value`>. ([#231](https://github.com/eerkunt/terraform-compliance/issues/231))
* Fixed a problem where `boolean` values where causing a problem on `Then its <key> <condition> be <value>`. ([#232](https://github.com/eerkunt/terraform-compliance/issues/232))
* Improved `When its <key> is <value>` steps for `reference` usage where you can provide a `key/value` check like `When its security_group_id reference is something`. ([#234](https://github.com/eerkunt/terraform-compliance/issues/234))
* Improved `When its <key> is not <value>` steps for `reference` usage where you can provide a `key/value` check like `When its security_group_id reference is not something`. ([#234](https://github.com/eerkunt/terraform-compliance/issues/234))
 
## 1.1.12 (2020-03-04)
* Improved `When its <key> contains <value>` step where `<value>` can have space in it. ([docs](https://terraform-compliance.com/pages/bdd-references/when.html#)) ([#226](https://github.com/eerkunt/terraform-compliance/issues/226))

## 1.1.11 (2020-03-04)
* Fixed a problem where `Then its <key> is <value>` step was not searching for "exact" matches. ([#225](https://github.com/eerkunt/terraform-compliance/issues/225))

## 1.1.10 (2020-03-03)
* Fixed a problem where int, bool and float types was not properly filtered and matched.
* Fixed a problem where filtering functions does not work properly.

## 1.1.9 (2020-02-25)
* Fixed a problem where a property within the terraform plan fails to get parsed if it is list of lists. ([#221](https://github.com/eerkunt/terraform-compliance/issues/221))

## 1.1.8 (2020-02-23)
* Fixed a problem where tags are not recognised on Auto-Scaling Groups due to different key/pair structure within the terraform. ([#208](https://github.com/eerkunt/terraform-compliance/issues/208))

## 1.1.7 (2020-02-06)
* Fixed a case where resource referencing fails when the output is coming from a module and does not registered in terraform plan.

## 1.1.6 (2020-02-04)
* Fixed a case sensitivity problem where some of the steps were running unexpectedly. ([#203](https://github.com/eerkunt/terraform-compliance/issues/203))

## 1.1.5 (2020-02-03)
* Added tags support on BDD feature files. As the first use case you can use @warning tag on top of a scenario for making it not failing. ([docs](https://terraform-compliance.com/pages/bdd-references/using_tags.html)) ([#191](https://github.com/eerkunt/terraform-compliance/issues/191))

## 1.1.4 (2020-02-03)
* Added a new environment variable `TFC_ERROR` to change the name of the default `Failure` error message. ([docs](https://terraform-compliance.com/pages/usage/environment_variables.html)) ([#191](https://github.com/eerkunt/terraform-compliance/issues/191))

## 1.1.3 (2020-02-01)
* Cosmetic and some dependency fixes.

## 1.1.2 (2020-02-01)
* Fixed an internal problem where a security group step will fail if there is no `cidr_blocks` definition within the plan. ([#198](https://github.com/eerkunt/terraform-compliance/issues/198))

## 1.1.0 (2020-02-01)

* New step: [Then it must have "something" referenced](https://terraform-compliance.com/pages/bdd-references/then.html#then-it-must-have-something-referenced). ([#195](https://github.com/eerkunt/terraform-compliance/issues/195))
* New step: [Then I flatten all values found](https://terraform-compliance.com/pages/bdd-references/then.html#then-i-flatten-all-values-found). ([#193](https://github.com/eerkunt/terraform-compliance/issues/193))
* New step: [Then its {key} must/must not be {value}](https://terraform-compliance.com/pages/bdd-references/then.html#its-key-condition-be-value).

* Security group revamp, which also addresses the problem defined in ([docs](https://terraform-compliance.com/pages/bdd-references/then.html#then--it-must-condition-have-proto-protocol-and-port-port-for-cidr)) ([#181](https://github.com/eerkunt/terraform-compliance/issues/181))
    * Security Group related code is rewritten, it is more flexible and extendable right now.
    * Security Group related tests now also have `must` condition where you may want to enforce if some subset of rules are defined in Security Groups.
    * Fixed a problem where `must only` and `must not` was not working properly when Security Groups have multiple rules attached. ([#181](https://github.com/eerkunt/terraform-compliance/issues/181))
* Now you can enforce rules for `output` variables. [#185](https://github.com/eerkunt/terraform-compliance/issues/185))

* New parameter: `-S/--silent` where test execution output will be suppressed. ([docs](https://terraform-compliance.com/pages/usage/#-S--silent))
* New parameter: `-n/--no-failure` where exit code will always be `0`/successful even there is a failure. ([docs](https://terraform-compliance.com/pages/usage/#-n--no-failure)) [#191](https://github.com/eerkunt/terraform-compliance/issues/191)
* New parameter: `-q/--quit-early` where the scenario executions will stop on the first failure. ([docs](https://terraform-compliance.com/pages/usage/#-q--quit-early)) [#170](https://github.com/eerkunt/terraform-compliance/issues/170)
* **CHANGE OF DEFAULT BEHAVIOUR** : `terraform-compliance` __will not__ STOP any test execution by default. 
* New emoticons and a bit of cosmetic make-up is done. All emoticons will be disabled on non-interactive shells (CI/CD pipelines) or if `--no-ansi` is explicitly used.

* Fixed `-h` which was not reporting all parameter properly
* Fixed a problem where `it contains` step was converting list of properties to dict of properties which was causing a problem. ([#194](https://github.com/eerkunt/terraform-compliance/issues/194))
* Fixed a problem where module outputs referencing a resource were not used on resource mounting. ([#190](https://github.com/eerkunt/terraform-compliance/issues/190))
* Fixed a problem where resources using `for_each` might cause some problems if `for_each` key includes `.` within. ([#197](https://github.com/eerkunt/terraform-compliance/issues/197))
* Fixed by overriding/monkey patching a method within [radish-bdd](https://github.com/radish-bdd/radish/issues/392) which enabled many other features.

### 1.0.60 (2019-12-28)
* Fixed a problem where some Windows Operating Systems could not find terraform executable. 

### 1.0.59 (2019-12-17)
* Fixed a problem where "resource" and "data" definitions existing for the same resource type in the same module causing some problems on all "GIVEN" steps. 

### 1.0.58 (2019-12-06)
* Enhanced `count` step where it was only applicable for resource properties, now it also works right after a `GIVEN` step. ([#187](https://github.com/eerkunt/terraform-compliance/issues/187)) 

### 1.0.57 (2019-11-15)
* Fixed a problem about encoding where `terraform-compliance` crashes on HCL files with UTF-8 content. ([#183](https://github.com/eerkunt/terraform-compliance/issues/183)) 

### 1.0.56 (2019-11-12)
* Removed `SKIPPED` lines if `dotter` formatter is used. (`--formatter dotter`) ([#180](https://github.com/eerkunt/terraform-compliance/issues/180)) 

### 1.0.55 (2019-11-05)
* Fixed a problem where filtering steps were failing on properly performing if the data is a list of dict of lists. E.g. `aws_iam_policy` with multiple heredoc policy statements. ([#177](https://github.com/eerkunt/terraform-compliance/issues/177))
* Added integration tests into the build pipeline for allowing end-to-end tests. 

### 1.0.54 (2019-10-30)
* Fixed a problem on providers discovery where some providers have alias, some doesn't. ([#173](https://github.com/eerkunt/terraform-compliance/issues/173))

### 1.0.53 (2019-10-30)
* Fixed a problem where resource names were reported wrong in some failures. ([#171](https://github.com/eerkunt/terraform-compliance/issues/171))
* Fixed a problem where in some cases `teraform-compliance` where giving `AttributeError: 'NoneType' object has no attribute 'get'` exception. ([#172](https://github.com/eerkunt/terraform-compliance/issues/172))
* Supporting multiple provider or providers aliases. ([#173](https://github.com/eerkunt/terraform-compliance/issues/173))
* Filtering steps are now performing case insensitive matching.
* Improved error messaged on steps doing math operations.

### 1.0.52 (2019-10-29)
* Fixed a problem where resource mounting were causing a issues on `resources that support tags`. ([#168](https://github.com/eerkunt/terraform-compliance/issues/168))

### 1.0.51 (2019-09-17)
* Fixed a problem where multiple resources were reported even some not failed. ([#153](https://github.com/eerkunt/terraform-compliance/issues/153))

### 1.0.50 (2019-09-16)
* Fixed a recursion problem occurred due to pointer assignment in resource mounting. ([#156](https://github.com/eerkunt/terraform-compliance/issues/156))
* Added a capability where some of the resource & property information was not shown in some tests. ([#153](https://github.com/eerkunt/terraform-compliance/issues/153))
* Added a capability where we can define ALL resources in GIVEN directive. ([#157](https://github.com/eerkunt/terraform-compliance/issues/157))
* Fixed a problem where `must` in a step does not trigger a failure for `provider`s. ([#158](https://github.com/eerkunt/terraform-compliance/issues/158))

### 1.0.49 (2019-09-08)
* Fixed a problem where resource mounting (via references) is done in both ways (A->B, B->A). This was causing a problem on `aws_instance` resource having an `iam_role` attached on it. ([#156](https://github.com/eerkunt/terraform-compliance/pull/156))

### 1.0.48 (2019-08-29)
* Fixed a problem where some resources can not be detected (or removed resources were still detected) due to plan changes. ([#152](https://github.com/eerkunt/terraform-compliance/pull/152))

### 1.0.47 (2019-08-27)
* This release includes several optimisations on CI/CD pipeline and the general build structure of the project.
* Using new version of Colorful dependency.

### 1.0.46 (2019-08-22)
* Fixed a problem where `gitphyton` was causing problems about installing `gitdb` python dependency.

### 1.0.45 (2019-08-20)
* Fixed intermittent `ImportError: cannot import name '__VERSION__' from 'radish'` problem.

### 1.0.44 (2019-08-16)
* Fixed a problem where using "" or '' was causing a problem on property definitions within the steps.

### 1.0.43 (2019-08-12)
* Fixed a problem where some of the filtering values were failing due to some characters.

### 1.0.42 (2019-08-10)
* Fixed a problem on CI/CD pipeline

### 1.0.41 (2019-08-10)
* Fixed a problem on CI/CD pipeline

### 1.0.40 (2019-08-10)
* Fixed a problem on CI/CD pipeline

### 1.0.39 (2019-08-09)
* Fix installing from source ([[#143](https://github.com/eerkunt/terraform-compliance/issues/143))

### 1.0.38 (2019-08-09)
* Support for `its value {condition} contain {value}`

### 1.0.37 (2019-08-09)
* Support for `equal` operator in `I expect the result is {operator} than/to {number}`
* Support for `its value {condition} be {value}`

### 1.0.36 (2019-08-09)
* Support for `any` resource in `I have {name} {type} configured`.
* Fixed some internals where `its {key} is {value}` and `its {key} is not {value}` might be mismatched unintentionally.

### 1.0.35 (2019-08-09)
* Upgraded colorful package to official version of 0.5.1 which solves the problem described in `1.0.31`
* Fixed naming conventions in the file. A new documentation with a website instead of just README is required though.

### 1.0.34 (2019-08-01)
* Now terraform-compliance has a logo!

### 1.0.33 (2019-07-31)
* Same like 1.0.32, but addressed another situation.

### 1.0.32 (2019-07-31)
* Fixed a problem where filtering via `its {key} is {value}` was failing if the filtering object consists list or dict.

### 1.0.31 (2019-07-30)
* Upgraded colourful that fixes unexpected colour coding in non-interactive terminals even when `--no-ansi` is used. ([#359](https://github.com/radish-bdd/radish/issues/359) [#128](https://github.com/eerkunt/terraform-compliance/issues/128) [#78](https://github.com/eerkunt/terraform-compliance/issues/78))

### 1.0.30 (2019-07-29)
* `its {key} is {value}` filtering step now filters also properties defined within a resource.

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
