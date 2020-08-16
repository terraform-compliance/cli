Feature: Feature for issue 338

	Scenario: Tag null
		Given I have resource that supports tags defined
		Then it must contain tags
		And its value must not be null


