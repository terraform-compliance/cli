# -*- coding: utf-8 -*-

from radish import step, arg_expr
import terraform_validate
import os
import sys

untaggable_resources = [
    "aws_route_table",
    "aws_elastic_beanstalk",
    "aws_security_group_rule",
    "aws_eip",
    "aws_nat_gateway",
    "aws_key_pair",
    "aws_lambda",
    "aws_iam",
    "aws_s3_bucket_notification",
    "aws_api_gateway",
    "aws_cloudfront_origin_access_identity",
    "aws_cloudwatch",
    "aws_server_certificate",
    "aws_route53_record",
    "aws_directory_service_directory",
    "azurerm_resource_group"
]

encryption_property = {
    "aws_db_instance": "storage_encrypted",
    "ebs_block_device": "encrypted",
    "aws_ebs_volume": "encrypted",
    "azurerm_storage_account": "enable_blob_encryption",
    "azurerm_sql_database": "encryption"
}

resource_name = {
    "AWS RDS instance": "aws_db_instance",
    "AWS EC2 instance": "aws_instance",
    "AWS EBS volume": "aws_ebs_volume",
    "AWS Security Group": "aws_security_group",
    "AWS Subnet": "aws_subnet",
    "Azure Storage Account": "azurerm_storage_account",
    "Azure SQL Database": "azurerm_sql_database",
    "resource that supports tags": "(?!{0}).*".format("|".join(untaggable_resources))
}

regex = {
    "Name": "^\${var.platform}_\${var.environment}_.*"
}

# New Arguments
@arg_expr("ANY", r"[\.\/_\-A-Za-z0-9\s]+")
def arg_exp_for_secure_text(text):
    return text

@step(r'Given I define {resource:ANY}')
def define_a_resource(step, resource):

    if(resource in resource_name.keys()):
        resource = resource_name[resource]

    step.context.resource_type = resource
    step.context.stash = step.context.resources = step.context.validator.resources(resource)

@step(r'When I {action:ANY} them')
def i_action_them(step, action):
    if action == "count":
        step.context.stash = len(step.context.stash.resource_list)
    elif action == "sum":
        step.context.stash = sum(step.context.stash.resource_list)
    else:
        AssertionError("Invalid action in the scenario: "+str(action))

@step(r'Then I expect the result is {operator:ANY} than {number:d}')
def i_expect_the_result_is_operator_than_number(step, operator, number):
    value = int(step.context.stash)

    if operator == "more":
        assert value > number, str(value)+" is not more than "+str(number)
    elif operator == "more and equal":
        assert value >= number, str(value)+" is not more and equal than "+str(number)
    elif operator == "less":
        assert value < number, str(value)+" is not less than "+str(number)
    elif operator == "less and equal":
        assert value <= number, str(value)+" is not less and equal than "+str(number)
    else:
        AssertionError("Invalid operator: "+str(operator))

@step('it contains {property:ANY}')
def it_contains_a(step, property):

    if(property in resource_name.keys()):
        property = resource_name[property]

    step.context.resource_type = property
    step.context.resources = step.context.resources.property(property)

@step('it must contain {property:ANY}')
def it_must_contain_a(step, property):
    step.context.validator.error_if_property_missing()
    if(property in resource_name.keys()):
        property = resource_name[property]

    step.context.resource_type = property
    step.context.resources = step.context.resources.property(property)

@step('encryption must be enabled')
def encryption_must_be_enabled(step):
    step.context.validator.error_if_property_missing()
    prop = encryption_property[step.context.resource_type]
    step.context.resources.property(prop).should_equal(True)


@step(u'it must have the "([^"]*)" tag')
def it_must_have_the_tag(step, tag):
    step.context.validator.error_if_property_missing()
    step.context.tag = tag
    step.context.properties = step.context.resources.property('tags')
    step.context.properties.should_have_properties(tag)


@step(u'And its value must match the "([^"]*)" regex')
def it_must_have_the_tag(step, regex_type):
    step.context.validator.error_if_property_missing()
    step.context.regex = regex[regex_type]
    step.context.properties.property(regex_type).should_match_regex(step.context.regex)

@step(u'And its value must be set by a variable')
def and_its_value_must_be_set_by_a_variable(step):
    step.context.resources.property('tags').property(step.context.tag).should_match_regex('\${var.(.*)}')

@step(r'with {proto:ANY} protocol and not port {value:d} for {cidr:ANY}')
def and_it_must_have_key_attribute_with_value_value(step, proto, value, cidr):
    proto = str(proto)
    value = int(value)
    cidr = str(cidr)

    giveError = False
    for i in step.context.resources.properties:
        protocol = ''
        from_port = 0
        to_port = 0
        cidr_blocks = False

        for y in i.property_value:

            if i.property_value[y] == proto:
                protocol = i.property_value[y]

            if y == 'from_port' and i.property_value[y] > 0:
                from_port = int(i.property_value[y])

            if y == 'to_port' and i.property_value[y] > 0:
                to_port = int(i.property_value[y])

            if y == 'cidr_blocks':
                if type(i.property_value[y] is list):
                    # There must be a CIDR check here.
                    # if cidr(parameter) is a member of given CIDR blocks,
                    # then accept it.
                    cidr_blocks = str(i.property_value[y][0])
                else:
                    cidr_blocks = str(i.property_value[y])



        if int(to_port) > int(from_port):
            if int(from_port) <= value <= int(to_port) and protocol == proto and cidr_blocks == cidr:
                giveError = True
        elif int(from_port) > int(to_port):
            if int(to_port) <= value <= int(from_port) or protocol == proto and cidr_blocks == cidr:
                giveError = True
        elif int(from_port) == int(to_port):
            if int(from_port) == value and protocol == proto and cidr_blocks == cidr:
                giveError = True

        if giveError:
            raise AssertionError("Found "+proto+"/"+str(value)+" for "+str(cidr_blocks))


