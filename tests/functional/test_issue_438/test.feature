Feature: Find resources which support a "non-default" property

# Given issue 438 is fixed 
#   And I have a aws_rds_cluster.db_cluster defined
#  When kms_key_id configured in the resource 
#  Then the resource aws_rds_cluster.db_cluster should be found
Scenario: Find resources which support a property when the property is not default
  Given I have resource that supports kms_key_id defined
  Then it must contain kms_key_id
