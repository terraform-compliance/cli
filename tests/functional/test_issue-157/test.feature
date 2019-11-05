Feature: EC2 containers should not have a role attached to them unless threat model requires it
  In order to improve security
  As engineers
  We'll not attach IAM Roles to EC2's unless otherwise Threat Modeled

  Scenario: Fail if a aws_instance has not been defined
    Given I have any resource defined
    When its type is aws_instance
    Then the scenario should fail

  Scenario: Fail if a VPC has not been defined
    Given I have any resource defined
    When its type is aws_vpc
    Then the scenario should fail
