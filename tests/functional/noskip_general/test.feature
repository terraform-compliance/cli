Feature: Feature for noskip
	@warning
	@noskip
	Scenario: This scenario should raise Failure: @warning and @noskip tags can not be used at the same time.
	        Given I have azurerm_resource_group defined
	        When its type is azurerm_postgresql_configuration
	        Then its type must be azurerm_postgresql_configuration

	@noskip
	Scenario: This scenario should raise Failure: Can not find azurerm_resource_group_bad defined in target terraform plan.
	        Given I have azurerm_resource_group_bad defined

	@noskip
	Scenario: This scenario should raise Failure: Can not find azurerm_postgresql_configuration type in azurerm_resource_group.example.
	        Given I have azurerm_resource_group defined
	        When its type is azurerm_postgresql_configuration
	        Then its type must be azurerm_postgresql_configuration

	@noskip
	Scenario: This scenario should pass
	        Given I have azurerm_postgresql_configuration defined
	        When its type is azurerm_postgresql_configuration
	        Then its type must be azurerm_postgresql_configuration
