Feature: Feature for issue #291

	@noskip
	Scenario: Ensure server parameter 'log_checkpoints' is set to 'ON' for PostgreSQL Database Server
	    Given I have azurerm_postgresql_server defined
		Given I have any resource defined
		When its type is azurerm_postgresql_configuration
	    Then it must contain value
	    And its value must match the "^(on)$|^([4-9]|\d{2,})$" regex

	@noskip_at_lines_15_22_23
	Scenario Outline: Scenario for issue #291
	    Given I have azurerm_postgresql_server defined
	    Given I have any resource defined
		When its type is azurerm_postgresql_configuration
        When its name is <config_name>
        Then it must have value
        Then its value must match the "<value>" regex

        Examples:
		| config_name        | value            |
		| log_checkpointsa    | on               |
		| log_retention_daysa | ^([4-9]\|\d{2,})$|