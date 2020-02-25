
resource "azurerm_virtual_machine" "elasticSearchVM" {
  name = "elasticSearchVM"
  os_profile_linux_config {
    disable_password_authentication = true
    ssh_keys {
      key_data = "ssh-rsa mykey"
      path = "/home/es/.ssh/authorized_keys"
    }
  }
  location = ""
  network_interface_ids = []
  resource_group_name = "test"
  vm_size = ""
  storage_os_disk {
    create_option = ""
    name = ""
  }
}
