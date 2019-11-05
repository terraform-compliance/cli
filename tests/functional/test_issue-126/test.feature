Feature:https://github.com/eerkunt/terraform-compliance/issues/126

#  Scenario: Ensure that aws-elb has listener ssl-cerificateid provided by Aws certificate Manager
#
#    Given I have AWS ELB resource defined
#    When it contains listener
#    Then it must contain ssl_certificate_id
#    And its value must match the ".*acm.*" regex


  Scenario: Ensure we are encryption ELBs via ACM.
    Given I have AWS ELB resource defined
    When it contains listener
    Then it must contain "ssl_certificate_id"
    And its value must match the ".*acm.*" regex

  Scenario: Ensure encryption flag is set on ELBs.
    Given I have AWS ELB resource defined
    When it contains listener
    Then it must contain 'ssl_certificate_id'
    And its value must not be null