Feature: Feature for issue #307

	@noskip
	Scenario: sns topic policy should not allow * principal - test2
	    Given I have aws_sns_topic_policy defined
		When it has policy
		And it has Statement
