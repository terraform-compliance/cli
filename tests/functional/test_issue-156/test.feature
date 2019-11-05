Feature: EC2 containers should not have a role attached to them unless threat model requires it
  In order to improve security
  As engineers
  We'll not attach IAM Roles to EC2's unless otherwise Threat Modeled

  Scenario: Fail if an EC2 has an IAM Role Attached to it
    Given I have AWS EC2 instance defined
    When it contains aws_iam_role
    Then the scenario should fail
