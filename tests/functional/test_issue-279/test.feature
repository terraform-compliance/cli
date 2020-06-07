Feature: ASG
  @warning
  Scenario: Health checks not enabled for ASG
    Given I have aws_autoscaling_group defined
    Then it must contain health_check_type
    And its value must match the "(^ELB$)|(^EC2$)" regex