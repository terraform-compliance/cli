variable "servicebus_queue_list" {
  default = [
      "something",
      "somethingelse",
      "somethingdifferent"
  ]
}

resource "azurerm_servicebus_queue" "sb" {
  for_each            = toset(var.servicebus_queue_list)
  name                = each.value
  resource_group_name = "testgroup"
  namespace_name      = "testnamespace"
  enable_partitioning = true
  dead_lettering_on_message_expiration = true
  default_message_ttl = "P14D"
}
