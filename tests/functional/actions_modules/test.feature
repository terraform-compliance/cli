Feature: Feature for issue 408, adding Terraform's actions to the resource
	Modules (with a slightly different test than for_each_and_modules)

	@noskip
  	Scenario: actions create
 		Given I have aws_iam_role defined
 		When its actions metadata has create

