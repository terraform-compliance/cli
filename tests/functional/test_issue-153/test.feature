Feature: Test Feature

  Scenario: Test Scenario
    Given I have aws_ebs_volume defined
    When it contains size
    Then Its value must be less than 45

