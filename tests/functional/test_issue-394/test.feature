Feature: feature for issue 394

	Scenario: Ensure storage accounts require private access to blob containers
	    Given I have azurerm_storage_account defined
	    When its name is not mystorageacct
	    Then it must contain allow_blob_public_access
	    And its value must be False
