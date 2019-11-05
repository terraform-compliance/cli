Feature: Help with "resource that supports tags"

  Scenario: Resource filtering on resource that support tags
    Given I have resource that supports tags defined
#    When its type is not aws_instance
    And it contains tags
    Then it must contain Name
    And its value must match the "terraform-compliance-test-156" regex
