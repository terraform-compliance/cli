Feature: test feature

#  @nofail
  Scenario: Unrestricted inbound access should not be allowed
    Given I have AWS Security Group defined
    When it contains ingress
    Then it must not have any protocol and port any for 0.0.0.0/0
