Feature: As the project is a Serverless project
  As Engineers, we want to limit the resources used
  within the project


Scenario Outline: Enforce resource existence
  Given I have <resource> defined
  Then the scenario should fail

  Examples:
  | resource              |
  | AWS Security Group    |
  | aws_vpc               |
  | aws_internet_gateway  |
  | aws_ec2_instance      |

