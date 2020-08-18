Feature: Feature for issue 343

    Scenario: Ensure all resources have tags
        Given I have resource that supports tags defined
        Then it must have tags
        And its value must not be null
