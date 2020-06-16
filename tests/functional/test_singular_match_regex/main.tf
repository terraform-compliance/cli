resource "azurerm_storage_account" "example" {
  name                     = "storageaccountname"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  network_rules {
    bypass                     = ["AzureServices", "Logging", "Metrics"]
    default_action             = "Deny"
    ip_rules                   = ["100.1.1.123/32"]
  }
  tags = {
    environment = "staging"
  }
}

resource "azurerm_storage_account" "example2" {
  name                     = "storageaccountname"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  network_rules {
    bypass                     = ["AzureServices", "Logging", "Metrics"]
    default_action             = "Deny"
    ip_rules                   = ["100.1.1.123/32"]
  }
  tags = {
    environment = "staging"
  }
}

resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "West Europe"
}

provider "azurerm" {
   features {}
}