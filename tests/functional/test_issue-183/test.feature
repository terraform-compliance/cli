Feature: Test

  Scenario : Only selected ports should be publicly open ingress success
    Given I have AWS Security Group defined
    When it contains ingress
    Then it must only have tcp protocol and port 53,80 for 0.0.0.0/0

  Scenario : Only selected ports should be publicly open ingress failure
    Given I have AWS Security Group defined
    When it contains ingress
    Then it must only have tcp protocol and port 53,80,123,443 for 0.0.0.0/0
