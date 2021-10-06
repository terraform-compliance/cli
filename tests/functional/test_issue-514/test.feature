Feature: VPC bug testing
    Scenario: VPC should have subnets mounted
        Given I have aws_vpc defined
        Then it must have aws_subnet

    Scenario: VPC should have network ACLs mounted
        Given I have aws_vpc defined
        Then it must have aws_network_acl

    Scenario: VPC subnets should have VPC mounted
        Given I have aws_subnet defined
        Then it must have aws_vpc

    Scenario: VPC subnets should have network ACLs mounted
        Given I have aws_subnet defined
        Then it must have aws_network_acl