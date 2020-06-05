# Fixed version of the features provided on issue 249
# Must not: Testing must not changes
Feature: Resources should be properly tagged
  In order to keep track of resource ownership
  As engineers
  We'll enforce tagging on all resources

# Check required tag for ALB and CF
  Scenario: Ensure that waf_policy for ALB/CF tag is defined
    Given I have aws_alb defined
    When it contains tags
    Then it must not contain waf_policy

  Scenario: Ensure that waf_custom for ALB/CF tag is defined
    Given I have aws_alb defined
    When it contains tags
    Then it must not contain waf_custom