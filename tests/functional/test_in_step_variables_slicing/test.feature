Feature: Testing slicing for in_step_variables using the Feature for issue #291
	supported list indexing slicing features:
	- [0]
	- [1:2]
	- [:]
	Works just like python's slicing.

	

	Scenario: slicing 1
		Given I have azurerm_postgresql_server defined
		Then it must have azurerm_postgresql_configuration
		Then it must have name
		Then it must be in {azurerm_postgresql_server.values.azurerm_postgresql_configuration.[:].name}


	Scenario: slicing 2
		Given I have azurerm_postgresql_server defined
		Then it must have azurerm_postgresql_configuration
		Then it must have name
		Then it must be in {azurerm_postgresql_server.values.azurerm_postgresql_configuration.[0:].name}


	Scenario: indexing
		Given I have azurerm_postgresql_server defined
		Then it must have azurerm_postgresql_configuration
		Then it must have name
		Then it must be in {azurerm_postgresql_server.values.azurerm_postgresql_configuration.[0].name}
