Feature: The scenarios defined below
	 require an MR review if any 
	 of the resources below exist 
	 in a plan 

Scenario Outline: changes to specific resources
    Given I have <resource> defined
    Then the scenario should fail 

    Examples:
      | resource                       |
      | aws_elasticache_security_group |
      | aws_default_security_group     |
      | aws_security_group             |
      | aws_security_group_rule        |
