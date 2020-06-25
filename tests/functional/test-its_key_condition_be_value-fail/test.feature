Feature: Feature for #291 continued
	Shoul fail, because not every resources type is azurerm_postgresql_configuration

	Scenario: Scenario for issue #291
	        Given I have any resource defined
	        Then its type must be azurerm_postgresql_configuration
