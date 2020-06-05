# Fixed version of the features provided on issue 249. 
# Bad feature: Last line changed to something that's not in tags
Feature: Resources should be properly tagged
  In order to keep track of resource ownership
  As engineers
  We'll enforce tagging on all resources

# Check required tag for ALB and CF
  Scenario: Ensure that waf_policy for ALB/CF tag is defined
    Given I have aws_alb defined
    When it contains tags
    Then it must contain waf_policy
    And its value must match the "^(internal|external|custom)$" regex

  Scenario: Ensure that waf_custom for ALB/CF tag is defined
    Given I have aws_alb defined
    When it contains tags
    Then it must contain bad_something_waf_custom