Feature: VPC Peering needs to follow compliance rules
  In order to have a valid VPC Peering
  As engineers
  We'll enforce vpc peering and routes have right information

  Scenario Outline: Owner and Peer Validation
    Given I have aws_vpc_peering_connection defined
    When it contains <key>
    Then its value must match the "<value>" regex

  Examples:
  | key           | value        |
  | peer_owner_id | 123456789    |
  | peer_vpc_id   | vpc-1a2b3c4d |