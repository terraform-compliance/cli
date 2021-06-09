---
layout: default
title: Overview of Scenario Flow
nav_order: 0
has_children: false
parent: BDD Reference
---
# Overview of Scenario Flow

## Basics

* __Terraform files__  contains the HCL that describes the infrastructure to be tested by terraform-compliance. Running `terraform plan --out=plan.out` creates a planfile (which is usally converted to a json planfile).
* __plan.out.json__ is the json file Terraform-Compliance uses to test your infrastructure. It resembles the terraform files closely, but there may be some differences depending on how used providers behave on `terraform plan`. Note that the plan file is a big nested dictionary. 
* Sometimes it's a good idea to search this file if you're unsure which words to use in your steps while writing scenarios. The context we refer to will usually be in configuration/root_module within the planfile

## Given and Context
Each step has a context. (i.e. list of resources, data this step will consider while deciding to pass or not) 

`GIVEN` sets the context, while `WHEN` and `THEN` narrows the context from the step above.

To begin a scenario, a `GIVEN` step must be used to set the initial context. Although it's less common, `GIVEN` can also be used to reset the context.

```
# Example 
#	if I have AWS VPC
#		then aws_flow_logs' must have traffic_type set to ALL

Scenario: VPC implies flowlogs' traffic_type is "ALL"
		Given I have aws_vpc defined
		Given I have aws_flow_log defined
		Then it must contain traffic_type
		And its value must be ALL
```
Here, I want to check a property of aws_flow_log resources, given I have aws_vpc. Therefore, I'm resetting the context to a new set of resources (aws_flow_log) instead of aws_vpc.

Most of the time, using preconditions or backgrounds are more suitable for cases using more than one Given.

While the the common Scenario structure looks like
```
    Given
    When
    ...
    Then
    ...
```

Given, When, Then steps could be used in any order.


## When
`WHEN` steps evaluate their condition and decide to pass or not. If the condition doesn't pass, it skips instead of failing.

Assume we had a plan of the following terraform file:
``` 
resource "azurerm_postgresql_server" "John" {
  ...
  auto_grow_enabled            = true
  ...
}
resource "azurerm_postgresql_server" "Douglas" {
  ...
  auto_grow_enabled            = false
  ...
}
```
The following steps would pass
```
Given I have azurerm_postgresql_server defined
When its auto_grow_enabled is true
```

### When filters
`WHEN` directive filters the context passed from the above step. Meaning if I have five elements in the context and only three of them satisfy the condition, I filter out (remove) the other two from the context and pass the remaining three elements unmodified.

In the above example, the context past the `GIVEN` step would be a list of both postgresql servers, while the context past the `WHEN` step would only be the first server.


If I didn't have any elements in the context that satisfied the condition, I would skip the scenario instead. 

If both servers had auto grow disabled, `When its auto_grow_enabled is true` would not be able to pass anything to the next step and would skip. `Given I have azurerm_postgresql_server defined`, its auto_grow_enabled is never set to true.

__Please note__, using `WHEN`, I can: filter a list of resource passed by `GIVEN`, filter an already filtered list of resource, filter a list of drilled down resources.)

## Then 
Similar to other steps, then also evaluates its condition and decides to pass or not. However if the condition doesn't pass, the scenario is failed. If then step is reached within a scenario, it is expected to pass. (Which usually is the very thing you're testing)

For example, the following scenario would fail on a plan where I have one aws_s3_bucket and one aws_flow_log defined.
``` 
Scenario: Example scenario
    Given I have any resource defined
	Then its type must be aws_flow_log
```
The first step would set the context to be a list of two resources: aws_s3_bucket and aws_flow_log. Since the type of s3 bucket is not aws_flow_log, the step fails.


### Then drills down
`THEN` steps drill down the current context.

A resource (or a provider, variable, etc.) is simply a nested dictionary. Drilling down changes the scope of that dictionary.


Let the following be one of the resources in the context and I want to check a value within the access_logs
``` 
{
	'data1': {
		...
	}
	'data2': {
		...
	}
	'access_logs': {
		bucket        = "foo"
	    bucket_prefix = "bar"
	    interval      = 60
	}

}
```
If I write `Then it has access_logs`, to the next step I will pass
```
{
	bucket        = "foo"
    bucket_prefix = "bar"
    interval      = 60
}
```
instead of the entire resource, as I "drilled down" into access_logs. If had used something like `When it has access_logs` I would pass the entire resource to the next step instead.

If the next step were to be `Then it has bucket`

I would drill down to:
```
"foo"
```

If I had a list of 5 resources similar to one above as my context and the `THEN` step passes, the context I'll be passing to the next step would be a list of 5 access_logs (the thing I drilled down to.)

The `THEN` directive fails the step if there's any element in the context that fails the condition (It can't drill down to one of the given elements in the context). So to pass a `THEN` step, all resources (whatever were drilled down to) must passs the step.

