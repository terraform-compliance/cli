# -*- coding: utf-8 -*-

from radish import step, world, custom_type, given, when, then
from terraform_compliance.steps import resource_name, encryption_property
from terraform_compliance.common.helper import check_sg_rules
from terraform_compliance.common.pyhcl_helper import parse_hcl_value
from terraform_compliance.extensions.terraform_validate import normalise_tag_values
from terraform_validate.terraform_validate import TerraformPropertyList, TerraformResourceList
from terraform_compliance.extensions.ext_radish_bdd import skip_step, step_condition, write_stdout
import re

# world.config.debug_steps = True


# New Arguments
@custom_type("ANY", r"[\.\/_\-A-Za-z0-9\s]+")
def custom_type_any(text):
    return text


@custom_type("SECTION", r"[a-z]+")
def custom_type_section(text):
    if text in ['resource', 'provider', 'data', 'module', 'output', 'terraform', 'variable']:
        return text

@custom_type("CONDITION", r"[a-z]+")
def custom_type_condition(text):
    if text in ['only', 'not']:
        return text

@given(u'I have {name:ANY} {type_name:SECTION} configured')
def i_have_name_section_configured(step_obj, name, type_name, radish_world=None):
    if radish_world is None:
        radish_world = world

    step_obj.context.type = type_name
    step_obj.context.name = name

    if type_name == "resource":
        if name in resource_name.keys():
            name = resource_name[name]

        found_resource = radish_world.config.terraform.resources(name)

        if hasattr(found_resource, 'resource_list') and found_resource.resource_list:
            step_obj.context.resource_type = name
            step_obj.context.defined_resource = name
            step_obj.context.stash = radish_world.config.terraform.resources(name)
        else:
            skip_step(step_obj, name)
    else:
        if type_name in radish_world.config.terraform.terraform_config:
            if name in radish_world.config.terraform.terraform_config[type_name]:
                step_obj.context.stash = radish_world.config.terraform.terraform_config[type_name][name]
            else:
                step_obj.context.stash = radish_world.config.terraform.terraform_config[type_name]

        else:
            skip_step(step_obj, type_name)


@given(u'I have {resource:ANY} defined')
def i_have_resource_defined(step_obj, resource, radish_world=None):
    if radish_world is None:
        radish_world = world

    if resource in resource_name.keys():
        resource = resource_name[resource]

    found_resource = radish_world.config.terraform.resources(resource)

    if found_resource.resource_list:
        step_obj.context.resource_type = resource
        step_obj.context.defined_resource = resource
        step_obj.context.stash = radish_world.config.terraform.resources(resource)
    else:
        skip_step(step_obj, '{} resource'.format(resource))


@when(u'I {action_type:ANY} them')
def i_action_them(step_obj, action_type):
    if action_type == "count":
        step_obj.context.stash = len(step_obj.context.stash.resource_list)
    elif action_type == "sum":
        # WARNING: Variable expansion & Interpolation might effect this result.
        step_obj.context.stash = sum([1 if type(b) is str else b for b in [resource.config.get('count', 1) for resource in step_obj.context.stash.resource_list]])
    else:
        AssertionError("Invalid action_type in the scenario: {}".format(action_type))


@then(u'I expect the result is {operator:ANY} than {number:d}')
def i_expect_the_result_is_operator_than_number(step_obj, operator, number):
    value = int(step_obj.context.stash)

    if operator == "more":
        assert value > number, "{} is not more than {}".format(value, number)
    elif operator == "more and equal":
        assert value >= number, "{} is not more and equal than {}".format(value, number)
    elif operator == "less":
        assert value < number, "{} is not less than {}".format(value, number)
    elif operator == "less and equal":
        assert value <= number, "{} is not less and equal than {}".format(value, number)
    else:
        AssertionError('Invalid operator: {}'.format(operator))


@when(u'it contain {something:ANY}')
@when(u'it contains {something:ANY}')
@then(u'it must contain {something:ANY}')
def it_condition_contain_something(step_obj, something,
                                   propertylist=TerraformPropertyList, resourcelist=TerraformResourceList):

    if something in resource_name.keys():
        something = resource_name[something]

    step_can_skip = step_condition(step_obj) in ["given", "when"]

    if step_obj.context.stash.__class__ is propertylist:
        for prop in step_obj.context.stash.properties:
            value = parse_hcl_value(prop.property_value, world.config.terraform.terraform_config)

            if value is not None:
                assert (value == something or something.lower() in value), \
                    '{} property in {} can not be found in {} ({}). It is set to {} instead'.format(something,
                                                                                                    prop.property_name,
                                                                                                    prop.resource_name,
                                                                                                    prop.resource_type,
                                                                                                    value)
            else:
                write_stdout(level='WARNING',
                             message='Can not get value of {} in {}/{}. '
                                     'Might be set by an unknown source (module, etc. )\n'
                                     'Value : {}'.format(something,
                                                         prop.property_name,
                                                         prop.resource_type,
                                                         prop.property_value))
                step_obj.state = 'skipped'

    elif step_obj.context.stash.__class__ is resourcelist:
        if step_can_skip is False:
            step_obj.context.stash.should_have_properties(something)
            step_obj.context.stash = step_obj.context.stash.find_property(something)
            assert step_obj.context.stash.properties, \
                'No defined property/value found for {}.'.format(something)
            step_obj.context.stash = step_obj.context.stash.properties
        else:
            try:
                step_obj.context.stash.should_have_properties(something)
                number_of_resources = len(step_obj.context.stash.resource_list)
                step_obj.context.stash = step_obj.context.stash.find_property(something)
                if step_obj.context.stash:
                    if number_of_resources > len(step_obj.context.stash.properties):
                        write_stdout(level='INFO',
                                     message='Some of the resources does not have {} property defined within.\n'
                                             'Removed {} resource (out of {}) from the test scope.\n'
                                             '\n'.format(something,
                                                         (number_of_resources-len(step_obj.context.stash.properties)),
                                                         number_of_resources,
                                                         ))
            except Exception as e:
                number_of_resources = len(step_obj.context.stash.resource_list)
                step_obj.context.stash = step_obj.context.stash.find_property(something)
                if step_obj.context.stash:
                    write_stdout(level='INFO',
                                 message='Some of the resources does not have {} property defined within.\n' 
                                         'Removed {} resource (out of {}) from the test scope.\n\n'
                                         'Due to : \n'
                                         '{}'.format(something,
                                                     (number_of_resources-len(step_obj.context.stash.properties)),
                                                     number_of_resources,
                                                     str(e)))
                else:
                    skip_step(step_obj,
                              resource=something,
                              message='Can not find {resource} property in any resource.')

    elif step_obj.context.stash.__class__ is dict:
        if something in step_obj.context.stash:
            step_obj.context.stash = step_obj.context.stash[something]
        else:
            if step_can_skip:
                skip_step(step_obj,
                          resource=something,
                          message='Can not find {resource} resource in terraform files.')
            else:
                assert False, '{} does not exist.'.format(something)


@then(u'encryption is enabled')
@then(u'encryption must be enabled')
def encryption_is_enabled(step_obj):
    prop = encryption_property[step_obj.context.resource_type]
    step_obj.context.stash.property(prop).should_equal(True)


@then(u'its value {condition:ANY} match the "{search_regex}" regex')
def its_value_condition_match_the_search_regex_regex(step_obj, condition, search_regex):
    regex = r'{}'.format(search_regex)

    if step_obj.context.stash.__class__ is str:
        matches = re.match(regex, step_obj.context.stash)

        if condition == 'must':
            assert matches is not None, \
                '{} {} tests failed on {} regex: {}'.format(step_obj.context.name,
                                                            step_obj.context.type,
                                                            regex,
                                                            step_obj.context.stash)
        elif condition == "must not":
            assert matches is None, \
                '{} {} tests failed on {} regex: {}'.format(step_obj.context.name,
                                                            step_obj.context.type,
                                                            regex,
                                                            step_obj.context.stash)
    else:
        normalise_tag_values(step_obj.context.stash)

        for prop in step_obj.context.stash.properties:
            if type(prop.property_value) is str:
                prop.property_value = [prop.property_value]
            elif type(prop.property_value) is dict:
                prop.property_value = prop.property_value.values()

            for value in prop.property_value:
                matches = re.match(regex, value)

                if condition == 'must':
                    assert matches is not None, \
                        '{} property in {} does not match with {} regex. It is set to {} instead.' \
                        ''.format(prop.property_name,
                                  prop.resource_name,
                                  search_regex,
                                  value)
                elif condition == 'must not':
                    assert matches is not None, \
                        '{} property in {} does not match with {} regex. It is set to {} instead.' \
                        ''.format(prop.property_name,
                                  prop.resource_name,
                                  search_regex,
                                  value)


@step(u'its value must be set by a variable')
def its_value_must_be_set_by_a_variable(step_obj):
    step_obj.context.stash.property(step_obj.context.search_value).should_match_regex(r'\${var.(.*)}')


@then(u'it must {condition:ANY} have {proto:ANY} protocol and port {port} for {cidr:ANY}')
def it_condition_have_proto_protocol_and_port_port_for_cidr(step_obj, condition, proto, port, cidr):
    proto = str(proto)
    cidr = str(cidr)
    ports = port

    # In case we have a range
    if '-' in port:
        from_port, to_port = port.split('-')
    # In case we have comma delimited ports
    elif ',' in port:
        from_port = to_port = '0'
        ports = port.split(',')
    else:
        from_port = to_port = port

    condition = condition == 'only'

    for item in step_obj.context.stash.properties:
        if type(item.property_value) is list:
            for security_group in item.property_value:
                check_sg_rules(world.config.terraform.terraform_config, security_group, condition, proto, from_port, to_port, ports, cidr)
        else:
            check_sg_rules(world.config.terraform.terraform_config, item.property_value, proto, condition, from_port, to_port, ports, cidr)
