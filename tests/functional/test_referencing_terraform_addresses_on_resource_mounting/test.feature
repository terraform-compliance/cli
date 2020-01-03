Feature: Test Feature

  Scenario: Test Scenario
    Given I have aws_instance defined
    When its address is aws_instance.test_instance
    Then it must have "^aws_security_group\.(test|mysql_in|pgsql_in)_sg$" referenced
