Feature: Ensure existing Then functionality of Terraform Compliance does not change

# Given issue 438 is fixed 
#   And there is a aws_rds_cluster defined
#  When it does not (or cannot) have and arn value configured
#  Then existing "then it must contain something" functionality is not changed
#   And the arn property will not be found on the aws_rds_cluster
Scenario: Then it must contain functionality not changed
  Given I have aws_rds_cluster defined
  Then it must contain arn

# Given issue 438 is fixed 
#   And I have a aws_rds_cluster defined
#  When it does not (or cannot) have and arn value configured
#  Then existing "then it must not contain something" functionality is not changed
#   And the arn property will not be found on the aws_rds_cluster
Scenario: Then it must not contain functionality not changed
  Given I have aws_rds_cluster defined
  Then it must not contain arn

# Given issue 438 is fixed 
#   And I have a aws_rds_cluster defined
#  When it does not (or cannot) have and arn value configured
#  Then existing "then any of its values must match the <regex> regex" functionality is not changed
#   And no values will be found that match "arn"
Scenario: Then any of its values must match regex functionality not changed
  Given I have aws_rds_cluster defined
  Then any of its values must match the "arn" regex
