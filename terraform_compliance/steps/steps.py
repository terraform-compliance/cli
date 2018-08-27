# -*- coding: utf-8 -*-

from radish import step, world, custom_type, then, when, given
from terraform_compliance.steps import untaggable_resources, regex, resource_name, encryption_property
from terraform_compliance.common.helper import check_sg_rules
from terraform_compliance.extensions.terraform_validate import normalise_tag_values


# New Arguments
@custom_type("ANY", r"[\.\/_\-A-Za-z0-9\s]+")
def arg_exp_for_secure_text(text):
    return text

@given(u'I have {resource:ANY} defined')
def define_a_resource(step, resource):
    world.config.terraform.error_if_property_missing()
    if (resource in resource_name.keys()):
        resource = resource_name[resource]

    step.context.resource_type = resource
    step.context.stash = step.context.resources = world.config.terraform.resources(resource)


@step(u'I {action_type:ANY} them')
def i_action_them(step, action_type):
    if not step.context.resources.resource_list:
        return

    if action_type == "count":
        step.context.stash = len(step.context.stash.resource_list)
    elif action_type == "sum":
        step.context.stash = sum(step.context.stash.resource_list)
    else:
        AssertionError("Invalid action_type in the scenario: {}".format(action))


@step(u'I expect the result is {operator:ANY} than {number:d}')
def func(step, operator, number):
    if not step.context.resources.resource_list:
        return

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


@step(u'it {condition:ANY} contain {something:ANY}')
def func(step, condition, something):
    if not step.context.resources.resource_list:
        return

    if condition == 'must':
        world.config.terraform.error_if_property_missing()

    if something in resource_name.keys():
        something = resource_name[something]

    step.context.resource_type = something
    step.context.resources = step.context.resources.property(something)

    if condition == 'must':
        assert step.context.resources.properties


@step(u'encryption is enabled')
@step(u'encryption must be enabled')
def func(step):
    if not step.context.resources.resource_list:
        return

    world.config.terraform.error_if_property_missing()
    prop = encryption_property[step.context.resource_type]
    step.context.resources.property(prop).should_equal(True)


@step(u'its value must match the "{regex_type}" regex')
def func(step, regex_type):
    if not step.context.resources.resource_list:
        return

    normalise_tag_values(step.context.properties)
    step.context.properties.property(regex_type).should_match_regex(step.context.regex)


@step(u'its value must be set by a variable')
def func(step):
    if not step.context.resources.resource_list:
        return

    step.context.resources.property(step.context.search_value).should_match_regex('\${var.(.*)}')


@step(u'it must not have {proto} protocol and port {port:d} for {cidr:ANY}')
def func(step, proto, port, cidr):
    proto = str(proto)
    port = int(port)
    cidr = str(cidr)

    for item in step.context.resources.properties:
        if type(item.property_value) is list:
            for security_group in item.property_value:
                check_sg_rules(world.config.terraform.terraform_config, security_group, proto, port, cidr)
        else:
            check_sg_rules(world.config.terraform.terraform_config, item.property_value, proto, port, cidr)