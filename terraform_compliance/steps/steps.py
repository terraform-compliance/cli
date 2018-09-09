# -*- coding: utf-8 -*-

from radish import step, world, custom_type, given
from terraform_compliance.steps import resource_name, encryption_property
from terraform_compliance.common.helper import check_sg_rules
from terraform_compliance.extensions.terraform_validate import normalise_tag_values


# New Arguments
@custom_type("ANY", r"[\.\/_\-A-Za-z0-9\s]+")
def arg_exp_for_secure_text(text):
    return text

@given(u'I have {resource:ANY} defined')
def define_a_resource(step, resource):
    if (resource in resource_name.keys()):
        resource = resource_name[resource]

    step.context.resource_type = resource
    step.context.stash = world.config.terraform.resources(resource)


@step(u'I {action_type:ANY} them')
def i_action_them(step, action_type):
    if hasattr(step.context.stash, 'resource_list') and not step.context.stash.resource_list:
        return

    if action_type == "count":
        step.context.stash = len(step.context.stash.resource_list)
    elif action_type == "sum":
        step.context.stash = sum(step.context.stash.resource_list)
    else:
        AssertionError("Invalid action_type in the scenario: {}".format(action_type))


@step(u'I expect the result is {operator:ANY} than {number:d}')
def i_expect_the_result_is(step, operator, number):
    if hasattr(step.context.stash, 'resource_list') and not step.context.stash.resource_list:
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
def it_contain(step, condition, something):
    if hasattr(step.context.stash, 'resource_list') and not step.context.stash.resource_list:
        return

    if condition == 'must':
        step.context.stash.should_have_properties(something)

    if something in resource_name.keys():
        something = resource_name[something]

    if type(something) not in [str, unicode]:
        step.context.resource_type = something

    step.context.stash = step.context.stash.property(something)

    if condition == 'must':
        assert step.context.stash.properties


@step(u'encryption is enabled')
@step(u'encryption must be enabled')
def encryption_is_enabled(step):
    if hasattr(step.context.stash, 'resource_list') and not step.context.stash.resource_list:
        return

    prop = encryption_property[step.context.resource_type]
    step.context.stash.property(prop).should_equal(True)


@step(u'its value must match the "{regex_type}" regex')
def func(step, regex_type):
    if  hasattr(step.context.stash, 'resource_list') or not step.context.stash.resource_list:
        return

    normalise_tag_values(step.context.properties)
    step.context.properties.property(regex_type).should_match_regex(step.context.regex)


@step(u'its value must be set by a variable')
def its_value_must_be_set_by_a_variable(step):
    if hasattr(step.context.stash, 'resource_list') and not step.context.stash.resource_list:
        return

    step.context.stash.property(step.context.search_value).should_match_regex(r'\${var.(.*)}')


@step(u'it must not have {proto} protocol and port {port:d} for {cidr:ANY}')
def it_must_not_have_sg_stuff(step, proto, port, cidr):
    proto = str(proto)
    port = int(port)
    cidr = str(cidr)

    for item in step.context.stash.properties:
        if type(item.property_value) is list:
            for security_group in item.property_value:
                check_sg_rules(world.config.terraform.terraform_config, security_group, proto, port, cidr)
        else:
            check_sg_rules(world.config.terraform.terraform_config, item.property_value, proto, port, cidr)