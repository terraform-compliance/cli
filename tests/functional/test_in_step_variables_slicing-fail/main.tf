resource "azurerm_resource_group" "example" {
  name     = "testingtfc-rg"
  location = "northeurope"
}

resource "azurerm_postgresql_server" "example" {
  name                         = "tfcpostgresql1111"
  location                     = azurerm_resource_group.example.location
  resource_group_name          = azurerm_resource_group.example.name
  sku_name                     = "B_Gen5_2"
  storage_mb                   = 5120
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true
  administrator_login          = "psqladminun"
  administrator_login_password = "H@Sh1CoR3!"
  version                      = "9.5"
  ssl_enforcement_enabled      = true
}

resource "azurerm_postgresql_configuration" "example" {
  name                = "log_checkpoints"
  resource_group_name = azurerm_resource_group.example.name
  server_name         = azurerm_postgresql_server.example.name
  value               = "on"
}

provider "azurerm" {
	features {}
}