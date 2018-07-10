Feature: Resources should be encrypted
  In order to improve security
  As engineers
  We'll enforce encryption

  Scenario: RDS instances
    When I define a AWS RDS instance
    Then encryption must be enabled

  Scenario: EC2 instance block devices
    When I define a AWS EC2 instance
    And it contains a ebs_block_device
    Then encryption must be enabled

  Scenario: EBS volumes
    When I define a AWS EBS volume
    Then encryption must be enabled
