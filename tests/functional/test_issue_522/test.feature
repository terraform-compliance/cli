Feature: Test

  Scenario: root_block_device must be configured on all non bastion hosts
    Given I have aws_instance defined
    When its name is not bastion
    Then it must have root_block_device
    And it must have encrypted
    And its value must be true

  Scenario: ebs_block_device, if present, must be configured on all non bastion hosts
    Given I have aws_instance defined
    When its name is not bastion
    When it has ebs_block_device
    Then it must have ebs_block_device
    Then it must have encrypted
    And its value must be true