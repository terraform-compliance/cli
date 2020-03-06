Feature: test

  Scenario: Images with environment in tag should be kept based on number of images with same environment
    Given I have aws_ecr_lifecycle_policy defined
    When it contains policy
    And it contains rules
    And its rulePriority is 10
    Then it must contain selection