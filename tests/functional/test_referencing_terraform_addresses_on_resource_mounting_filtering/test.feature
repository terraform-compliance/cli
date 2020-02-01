Feature: Test Feature

  Scenario: Test Scenario
    Given I have aws_instance defined
    When its reference is aws_security_group.test_sg
    Then it must fail
