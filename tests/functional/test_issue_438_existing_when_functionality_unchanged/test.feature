Feature: Ensure existing When functionality of Terraform Compliance does not change

# Given issue 438 is fixed 
#   And I have a aws_rds_cluster defined
#  When it does not (or cannot) have and arn value configured
#  Then existing "when it contains something" functionality is not changed
#   And the arn property will not be found on the aws_rds_cluster
Scenario: When it does contain functionality not changed
  Given I have aws_rds_cluster defined
  When it contains arn

# Given issue 438 is fixed 
#   And I have a aws_rds_cluster defined
#  When it does not (or cannot) have and arn value configured
#  Then existing "when it does not contains something" functionality is not changed
#   And the arn property will not be found on the aws_rds_cluster
Scenario: When it does not contain functionality not changed
  Given I have aws_rds_cluster defined
  When it does not contain arn

# Given issue 438 is fixed 
#   And I have a aws_rds_cluster defined
#  When it does not (or cannot) have and id value configured
#  Then existing "when it has something" functionality is not changed
#   And the id property will not be found on the aws_rds_cluster
Scenario: When it has functionality not changed
  Given I have aws_rds_cluster defined
  When it has id
