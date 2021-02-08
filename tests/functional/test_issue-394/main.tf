provider "azurerm" {
	features {}
}


resource "azurerm_storage_account" "example" {
  name                     = "mystorageacct"
  resource_group_name      = "example"
  account_tier             = "Standard"
  location                 = "East US"
  account_replication_type = "LRS"
  allow_blob_public_access = true
}
resource "azurerm_storage_account" "private" {
  name                     = "myprivatestorageacct"
  resource_group_name      = "example"
  account_tier             = "Standard"
  location                 = "East US"
  account_replication_type = "LRS"
  allow_blob_public_access = false
}
