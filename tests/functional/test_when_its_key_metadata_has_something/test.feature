Feature: Feature for issue 408

 	Scenario: metadata does not have
 		Given I have aws_instance defined
 		When its actions metadata does not have no-op
 		Then it must have instance_type 
 
 	Scenario: metadata has
 		Given I have aws_instance defined
 		When its actions metadata has create
 		Then it must have instance_type
 
  	Scenario: metadata has (should skip)
 		Given I have aws_s3_bucket defined
 		When its actions metadata has create
 		Then its acl must be private
 
 	@noskip
	Scenario: Scenario for issue 408 4
		Given I have aws_instance defined
		When its address metadata is aws_instance.unchanged

