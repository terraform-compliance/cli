Feature: Feature for issue 408, adding Terraform's actions to the resource

	@noskip
 	Scenario: actions no-op
 		Given I have aws_instance defined
 		When its actions metadata has no-op
 		Then it must have instance_type 
 
	@noskip
 	Scenario: actions update
 		Given I have aws_instance defined
 		When its actions metadata has update
 		Then it must have instance_type 
 
 	@noskip
  	Scenario: actions create
 		Given I have aws_s3_bucket defined
 		When its actions metadata has create
 		Then its acl must be private
