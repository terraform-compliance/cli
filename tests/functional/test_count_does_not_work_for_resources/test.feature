Feature: test for https://github.com/eerkunt/terraform-compliance/issues/187

  Scenario Outline: Ensure that specific tags are defined
     Given I have aws_autoscaling_group defined
     When it has tags
     Then it must contain <tags>
     And its value must match "^(webtier|apptier|datatier)" regex
