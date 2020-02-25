Feature: Test

  Scenario: ElasticSearch VM linux config
    Given I have azurerm_virtual_machine defined
    When its address is module.elasticSearch.azurerm_virtual_machine.elasticSearchVM
    Then it must contain os_profile_linux_config
    And it must contain disable_password_authentication
    And its value must be true

  Scenario Outline: ElasticSearch VM linux config ssh
    Given I have azurerm_virtual_machine defined
    When its address is module.elasticSearch.azurerm_virtual_machine.elasticSearchVM
    Then it must contain os_profile_linux_config
    And it must contain ssh_keys
    And it must contain <key>
    And its value must be <value>

    Examples:
    | key  | value                              |
    | key_data | ssh-rsa mykey                  |
    | path | /home/es/.ssh/authorized_keys |
