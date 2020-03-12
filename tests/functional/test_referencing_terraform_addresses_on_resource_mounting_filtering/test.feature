Feature: Test Feature

  Scenario: Test Scenario - should fail
    Given I have aws_instance defined
    When its reference is aws_security_group.test_sg
    Then it must fail

  Scenario: Test Scenario with key-value - should fail
    Given I have aws_instance defined
    When its vpc_security_group_ids reference is aws_security_group.test_sg
    Then it must fail

  Scenario: Test Scenario - should skip
    Given I have aws_instance defined
    When its reference is aws_security_group.ab
    Then it must fail

  Scenario: Test Scenario with key-value - should skip
    Given I have aws_instance defined
    When its something reference is aws_security_group.test_sg
    Then it must fail

  Scenario: Test Negative Scenario - should fail
    Given I have aws_instance defined
    When its reference is not aws_security_group.abc
    Then it must fail

  Scenario: Test Negative Scenario key-value - should fail
    Given I have aws_instance defined
    When its vpc_security_group_ids reference is not aws_security_group.abc
    Then it must fail

  Scenario: Test Negative Scenario - should skip
    Given I have aws_instance defined
    When its reference is not aws_security_group.test_sg
    Then it must fail

  Scenario: Test Negative Scenario key-value - should skip
    Given I have aws_instance defined
    When its vpc_security_group_ids reference is not aws_security_group.test_sg
    Then it must fail