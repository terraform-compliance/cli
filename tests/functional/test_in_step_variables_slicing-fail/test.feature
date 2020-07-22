Feature: Testing slicing for in_step_variables using the Feature for issue #291
	Bad slicing should return an empty list instead of breaking the test.


	Scenario: indexing bad
		Given I have azurerm_postgresql_server defined
		Then it must have azurerm_postgresql_configuration
		Then it must have name
		Then it must be in {azurerm_postgresql_server.values.azurerm_postgresql_configuration.[4:2].name}

