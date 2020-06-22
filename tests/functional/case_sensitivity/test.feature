Feature: Feature for #291 continued
	Shoul fail, because not every resources type is azurerm_postgresql_configuration

	@case_sensitive
	Scenario: Then it must contain (fails)
	        Given I have azurerm_postgresql_server defined
	        Then it must contain SKU_NAME


	@case_sensitive
	Scenario: Then it must not contain (passes)
	        Given I have azurerm_postgresql_server defined
	        Then it must not contain SKU_NAME


	@case_sensitive
	Scenario: Then its value must contain (fails)
	        Given I have azurerm_postgresql_server defined
	        Then it must contain sku_name
	        And its value must contain B_GEN5_2


	@case_sensitive
	Scenario: Then its value must contain (passes)
	        Given I have azurerm_postgresql_server defined
	        Then it must contain sku_name
	        And its value must contain B_Gen5_2


	@case_sensitive
	Scenario: Then its key condition be value (fails - value)
	        Given I have azurerm_postgresql_configuration defined
	        Then its type must be azurerm_postgresql_configuratioN


	@case_sensitive
	Scenario: Then its key condition be value (passes)
	        Given I have azurerm_postgresql_configuration defined
	        Then its sku_name must be B_Gen5_2


	@case_sensitive
	Scenario: Then its key condition be value (fails - key)
	        Given I have azurerm_postgresql_configuration defined
	        Then its sku_Name must be B_Gen5_2


	@case_sensitive
	Scenario: Then its value condition contain (passes)
	        Given I have azurerm_postgresql_configuration defined
	        Then it must have sku_name
	        And its value must match the "B_Gen5_2" regex


	@case_sensitive
	Scenario: Then its value condition contain (fails)
	        Given I have azurerm_postgresql_configuration defined
	        Then it must have sku_name
	        And its value must match the "B_GeN5_2" regex


	@case_sensitive
	Scenario: Then property is enabled (passes)
	        Given I have azurerm_postgresql_configuration defined
	        Then sku_name is be enabled

	@case_sensitive
	Scenario: Then property is enabled (fails)
	        Given I have azurerm_postgresql_configuration defined
	        Then sku_namE is be enabled


	@noskip        
	@case_sensitive
	Scenario: When it contains (pass)
	        Given I have azurerm_postgresql_configuration defined
	        When it contains sku_name


	@noskip
	@case_sensitive
	Scenario: When it contains (fails)
	        Given I have azurerm_postgresql_configuration defined
	        When it contains sku_namE



	@noskip
	@case_sensitive
	Scenario: When it has (pass)
	        Given I have azurerm_postgresql_configuration defined
	        When it has sku_name


	@noskip
	@case_sensitive
	Scenario: When it has (fails)
	        Given I have azurerm_postgresql_configuration defined
	        When it has sku_namE


	@noskip	        
	@case_sensitive
	Scenario: When it does not have (pass)
	        Given I have azurerm_postgresql_configuration defined
	        When it does not have sku_namE


	@noskip
	@case_sensitive
	Scenario: When it does not have (fails)
	        Given I have azurerm_postgresql_configuration defined
	        When it does not have sku_name


	@noskip
	@case_sensitive
	Scenario: When its key is value (pass)
	        Given I have azurerm_postgresql_server defined
	        When its sku_name is B_Gen5_2


	@noskip
	@case_sensitive
	Scenario: When its key is value (fails - key)
	        Given I have azurerm_postgresql_server defined
	        When its sku_namE is B_Gen5_2


	@noskip
	@case_sensitive
	Scenario: When its key is value (fails - value)
	        Given I have azurerm_postgresql_server defined
	        When its sku_name is B_GeN5_2


	# what I would test for maths is already tested in current tests

	@noskip
	@case_sensitive
	Scenario: Given I have resource defined (passes)
	        Given I have azurerm_postgresql_server defined



	@noskip
	@case_sensitive
	Scenario: Given I have resource defined (fails)
	        Given I have azurerm_postgresql_serveR defined


	@noskip
	Scenario: Given I have resource defined (just making sure this passes)
	        Given I have azurerm_postgresql_serveR defined



	@noskip
	@case_sensitive
	Scenario: Given I have provider configured (passes)
	        Given I have azurerm provider configured


	@noskip
	@case_sensitive
	Scenario: Given I have provider configured (fails)
	        Given I have azurerM provider configured
