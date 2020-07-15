Feature: Feature for issue #285
	@noskip_at_line_7
	Scenario: Ensure 'Trusted Microsoft Services' is enabled for Storage Account access
		Given I have azurerm_storage_account defined
		Then it must contain network_rules
		And it must contain bypass
		When it has AzureServices
		Then any of its values must match the "(^AzureServicesBad$)" regex