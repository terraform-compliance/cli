Feature: Feature for #537
  Test

  Scenario Outline: Ensure all ASGs have tags
    Given I have aws_autoscaling_group defined
    When it has tags
    Then it must contain <tags>
    And its value must match the "^(webtier|apptier|datatier)" regex


    Examples:
      | tags |
      | Tier |pytes
