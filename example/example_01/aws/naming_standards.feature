Feature: Resources should have a proper naming standard
  In order to keep consistency between resources
  As engineers
  We'll enforce naming standards

  Scenario Outline: Naming Standard on all available resources
    Given I have <resource_name> defined
    When it contains <name_key>
    Then its value must match the "\${var.project}-\${var.environment}-\${var.application}-.*" regex

    Examples:
    | resource_name           | name_key |
    | AWS EC2 instance        | name     |
    | AWS ELB resource        | name     |
    | AWS RDS instance        | name     |
    | AWS S3 Bucket           | name     |
    | AWS EBS volume          | name     |
    | AWS Auto-Scaling Group  | name     |
    | aws_key_pair            | key_name |
    | aws_ecs_cluster         | name     |
