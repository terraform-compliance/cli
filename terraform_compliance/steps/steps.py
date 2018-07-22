# -*- coding: utf-8 -*-

from radish import step, world, custom_type, then, when, given
from terraform_compliance.steps import untaggable_resources, regex, resource_name, encryption_property
from terraform_compliance.common.helper import check_port_cidr_ranges


# New Arguments
@custom_type("ANY", r"[\.\/_\-A-Za-z0-9\s]+")
def arg_exp_for_secure_text(text):
    return text


@step(u'I define an {resource:ANY}')
@step(u'I define a {resource:ANY}')
@step(u'I define {resource:ANY}')
def define_a_resource(step, resource):
    world.config.terraform.error_if_property_missing()
    if (resource in resource_name.keys()):
        resource = resource_name[resource]

    step.context.resource_type = resource
    step.context.stash = step.context.resources = world.config.terraform.resources(resource)


@step(u'I {action_type:ANY} them')
def i_action_them(step, action_type):
    if action_type == "count":
        step.context.stash = len(step.context.stash.resource_list)
    elif action_type == "sum":
        step.context.stash = sum(step.context.stash.resource_list)
    else:
        AssertionError("Invalid action_type in the scenario: {}".format(action))


@step(u'I expect the result is {operator:ANY} than {number:d}')
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


@step(u'it must contain {something:ANY}')
def func(step, something):
    world.config.terraform.error_if_property_missing()

    if something in resource_name.keys():
        something = resource_name[something]

    step.context.resource_type = something
    step.context.resources = step.context.resources.property(something)

@step(u'it contains {something:ANY}')
def func(step, something):
    if something in resource_name.keys():
        something = resource_name[something]

    step.context.resource_type = something
    step.context.resources = step.context.resources.property(something)

@step(u'encryption is enabled')
@step(u'encryption must be enabled')
def func(step):
    world.config.terraform.error_if_property_missing()
    prop = encryption_property[step.context.resource_type]
    step.context.resources.property(prop).should_equal(True)


@step(u'it must have the "{tag:ANY}" tag')
def func(step, tag):
    world.config.terraform.error_if_property_missing()
    step.context.tag = tag
    step.context.properties = step.context.resources.property('tags')
    step.context.properties.should_have_properties(tag)


@step(u'its value must match the "{regex_type}" regex')
def func(step, regex_type):
    world.config.terraform.error_if_property_missing()
    step.context.regex = regex[regex_type]
    step.context.properties.property(regex_type).should_match_regex(step.context.regex)


@step(u'its value must be set by a variable')
def func(step):
    step.context.resources.property('tags').property(step.context.tag).should_match_regex('\${var.(.*)}')


@step(u'with {proto} protocol and not port {port:d} for {cidr:ANY}')
def func(step, proto, port, cidr):
    proto = str(proto)
    port = int(port)
    cidr = str(cidr)

    for item in step.context.resources.properties:
        if type(item.property_value) is list:
            for security_group in item.property_value:
                check_port_cidr_ranges(world.config.terraform.terraform_config, security_group, proto, port, cidr)
        else:
            check_port_cidr_ranges(world.config.terraform.terraform_config, item.property_value, proto, port, cidr)