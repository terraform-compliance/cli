Feature: test

  Scenario: Ensure we have service tag for live environments
    Given I have resource that supports tags defined
#    When its type is not aws_autoscaling_group
    When it contains tags
    And its environment is live
    Then it must contain service
    And its value must not be null

