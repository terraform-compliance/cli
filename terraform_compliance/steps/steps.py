# -*- coding: utf-8 -*-

from radish import step, world, custom_type

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
@custom_type("ANY", r"[\.\/_\-A-Za-z0-9\s]+")
def arg_exp_for_secure_text(text):
    return text

@step(r'Given I define {resource}')
def define_a_resource(step, resource):
    if (resource in resource_name.keys()):
        resource = resource_name[resource]

    step.context.resource_type = resource
    step.context.stash = step.context.resources = world.config.terraform.resources(resource)


@step(r'When I {action_type} them')
def i_action_them(step, action_type):
    if action_type == "count":
        step.context.stash = len(step.context.stash.resource_list)
    elif action_type == "sum":
        step.context.stash = sum(step.context.stash.resource_list)
    else:
        AssertionError("Invalid action_type in the scenario: {}".format(action))


@step(r'Then I expect the result is {operator} than {number:d}')
def func(step, operator, number):
    value = int(step.context.stash)

    if operator == "more":
        assert value > number, str(value) + " is not more than " + str(number)
    elif operator == "more and equal":
        assert value >= number, str(value) + " is not more and equal than " + str(number)
    elif operator == "less":
        assert value < number, str(value) + " is not less than " + str(number)
    elif operator == "less and equal":
        assert value <= number, str(value) + " is not less and equal than " + str(number)
    else:
        AssertionError("Invalid operator: " + str(operator))


@step('it must contain {something}')
def func(step, something):
    world.config.terraform.error_if_property_missing()

    if something in resource_name.keys():
        something = resource_name[something]

    step.context.resource_type = something
    step.context.resources = step.context.resources.property(something)


@step('encryption must be enabled')
def func(step):
    world.config.terraform.error_if_property_missing()
    prop = encryption_property[step.context.resource_type]
    step.context.resources.property(prop).should_equal(True)


@step(u'it must have the "([^"]*)" tag')
def func(step, tag):
    world.config.terraform.error_if_property_missing()
    step.context.tag = tag
    step.context.properties = step.context.resources.property('tags')
    step.context.properties.should_have_properties(tag)


@step(u'And its value must match the "([^"]*)" regex')
def func(step, regex_type):
    world.config.terraform.error_if_property_missing()
    step.context.regex = regex[regex_type]
    step.context.properties.property(regex_type).should_match_regex(step.context.regex)


@step(u'And its value must be set by a variable')
def func(step):
    step.context.resources.property('tags').property(step.context.tag).should_match_regex('\${var.(.*)}')


@step(r'with {proto} protocol and not port {port} for {cidr}')
def func(step, proto, port, cidr):
    proto = str(proto)
    port = int(port)
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
            if int(from_port) <= port <= int(to_port) and protocol == proto and cidr_blocks == cidr:
                giveError = True
        elif int(from_port) > int(to_port):
            if int(to_port) <= port <= int(from_port) or protocol == proto and cidr_blocks == cidr:
                giveError = True
        elif int(from_port) == int(to_port):
            if int(from_port) == port and protocol == proto and cidr_blocks == cidr:
                giveError = True

        if giveError:
            raise AssertionError("Found " + proto + "/" + str(port) + " for " + str(cidr_blocks))
