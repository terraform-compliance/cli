Feature: API Gateway related general feature
         This feature will ;
         - Check if API Gateway REST or WebSocket API stages have relevant logs enabled. 
           To meet this check criteria, use aws-apigw-rest module 
           (https://github.com/cmctechnology/cc-tf-modules/tree/master/aws-apigw-rest, minimum supported version 15.0.3) 
    
    Scenario: Check if cloudwatch role is added to API Gateway on account level
       Given I have aws_api_gateway_account defined
       Then it must contain cloudwatch_role_arn
       And its value must not be null

    Scenario: Check if logging is enabled on API Gateway Stage method settings 
        Given I have aws_api_gateway_method_settings defined
        Then it must contain logging_level
        And its value must not be OFF