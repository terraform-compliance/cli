Feature: Feature for noskip
	@noskip
	@no-skip_at_line_4
	Scenario: Scenario for noskip
	        Given I have azurerm_resource_group defined
	        When its type is azurerm_postgresql_configuration
	        Then its type must be azurerm_postgresql_configuration
