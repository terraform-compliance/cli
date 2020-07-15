Feature: Feature for issue #307
	Lazy naming.
	First scenario tests the jsonification changes.
	Other scenarios also tests changes to drill-down on Then it must contain

	@noskip
	Scenario: Jsonficiation changes
	    Given I have aws_sns_topic_policy defined
		When it has policy
		And it has Statement

	@noskip
	Scenario: sns topic policy should not allow * principal - test1
		Given I have aws_sns_topic_policy defined
		When it contains policy
		And it contains Statement
		And its Effect is Allow
		Then it must contain Principal
		And its value must not match the "\*$" regex

	@noskip		
	Scenario: sns topic policy should not allow * principal - test2
	    Given I have aws_sns_topic_policy defined
		When it has policy
		And it has Statement
		Then it must have Statement
		When its Effect is Allow
		Then it must contain Principal
		And its value must not match the "\*$" regex
		
	@noskip
	Scenario Outline: sns topic policy should not allow * principal - test3
		Given I have aws_sns_topic_policy defined
		When it has policy
		Then it must contain policy
		Then it must contain Statement
		Then it must contain <key> 
		And its value <condition> match the "<value>" regex

	Examples:
	| key        | condition    | value    |
	| Effect     | must         | Allow    |
	| Principal  | must not     |  ^\\*$    |


	@noskip
	Scenario: sns topic policy should not allow * principal - test3 effect
        Given I have aws_sns_topic_policy defined
		When it has policy
		Then it must contain policy
		Then it must contain Statement
		Then it must contain Effect
		And its value must match the "Allow" regex


	@noskip
	Scenario: sns topic policy should not allow * principal - test3 principal
        Given I have aws_sns_topic_policy defined
		When it has policy
		Then it must contain policy
		Then it must contain Statement
		Then it must contain Principal
		And its value must not match the "^\*$" regex