Feature: Resources should be properly tagged
  In order to keep track of resource ownership
  As engineers
  We'll enforce tagging on all resources

  Scenario: Name tag
    When I define a resource that supports tags
    Then it must have the "Name" tag
    And its value must match the "darwin.*" regex

  Scenario: Environment tag
    When I define a resource that supports tags
    Then it must have the "Environment" tag
    And its value must be set by a variable

  Scenario: Project tag
    When I define a resource that supports tags
    Then it must have the "Project" tag
    And its value must match the "Darwin" regex

  Scenario: Service tag
    When I define a resource that supports tags
    Then it must have the "Service" tag
    And its value must match the "modelling|enhancement|routing|scoring" regex

  Scenario: Function tag
    When I define a resource that supports tags
    Then it must have the "Function" tag

  Scenario: Billing tag
    When I define a resource that supports tags
    Then it must have the "Billing" tag
