# -*- coding: utf-8 -*-

from radish import step, world, given, when, then
from terraform_compliance.steps import encryption_property
from terraform_compliance.common.helper import check_sg_rules, convert_resource_type
from terraform_compliance.extensions.ext_radish_bdd import (
    skip_step,
    step_condition,
    write_stdout,
    custom_type_section,
    custom_type_any,
    custom_type_condition
)
import re

# world.config.debug_steps = True

#TODO: WRITE ALL STEPS FROM SCRATCH!!!

@given(u'I have {name:ANY} defined')
@given(u'I have {name:ANY} {type_name:SECTION} configured')
def i_have_name_section_configured(_step_obj, name, type_name='resource', _terraform_config=world):
    '''
    Finds given resource or variable by name and returns it. Skips the step (and further steps) if it is not found.

    :param _step_obj: Internal, step object for radish.
    :param name: String of the name of the resource_type or variable.
    :param type_name: String of the type, either resource(s) or variable(s)
    :param _terraform_config: Internal, terraform configuration.
    :return:
    '''
    print('Step> {}'.format(_step_obj.context_sensitive_sentence))

    assert (type_name in ['resource', 'resources', 'variable', 'variables']), \
        '{} configuration type does not exist or not implemented yet. ' \
        'Use resource(s) or variable(s) instead.'.format(type_name)

    if type_name.endswith('s'):
        type_name = type_name[:-1]

    if type_name == 'resource':
        name = convert_resource_type(name)
        resource_list = _terraform_config.config.terraform.find_resources_by_type(name)

        if resource_list:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = resource_list
            return

    elif type_name == 'variable':
        found_variable = _terraform_config.config.terraform['variables'].get(name, None)

        if found_variable:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = found_variable
            return

    skip_step(_step_obj, name)

@when(u'I {action_type:ANY} them')
def i_action_them(_step_obj, action_type):
    print('Step> {}'.format(_step_obj.context_sensitive_sentence))


@then(u'I expect the result is {operator:ANY} than {number:d}')
def i_expect_the_result_is_operator_than_number(_step_obj, operator, number):
    print('Step> {}'.format(_step_obj.context_sensitive_sentence))

@when(u'it contain {something:ANY}')
@when(u'it contains {something:ANY}')
@then(u'it must contain {something:ANY}')
def it_condition_contain_something(_step_obj, something):
    print('Step> {}'.format(_step_obj.context_sensitive_sentence))
    property_list = []

    if _step_obj.context.type == 'resource':
        for property in _step_obj.context.stash:
            if property.get('values', {}).get(something, None):
                property_list.extend(property['values'][something])

        if property_list:
            _step_obj.context.stash = property_list
            return

        skip_step(_step_obj,
                  resource=_step_obj.context.name,
                  message='Can not find any {} property for {} resource in '
                          'terraform files.'.format(something, _step_obj.context.name))

    skip_step(_step_obj,
              resource=_step_obj.context.name,
              message='Skipping the step since {} type does not have any property.'.format(_step_obj.context.type))


@then(u'encryption is enabled')
@then(u'encryption must be enabled')
def encryption_is_enabled(_step_obj):
    print('Step> {}'.format(_step_obj.context_sensitive_sentence))

@then(u'its value {condition:ANY} match the "{search_regex}" regex')
def its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex):
    print('Step> {}'.format(_step_obj.context_sensitive_sentence))

@step(u'its value must be set by a variable')
def its_value_must_be_set_by_a_variable(_step_obj):
    print('Step> {}'.format(_step_obj.context_sensitive_sentence))

@then(u'it must {condition:ANY} have {proto:ANY} protocol and port {port} for {cidr:ANY}')
def it_condition_have_proto_protocol_and_port_port_for_cidr(_step_obj, condition, proto, port, cidr):
    print('Step> {}'.format(_step_obj.context_sensitive_sentence))
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

    plan_data = dict(proto=proto,
                     from_port=from_port,
                     to_port=to_port,
                     ports=ports,
                     cidr=cidr)

    for security_group in _step_obj.context.stash:
        check_sg_rules(security_group, condition, plan_data)


# @when(u'I {action_type:ANY} them')
# def i_action_them(_step_obj, action_type):
#     if action_type == "count":
#         _step_obj.context.stash = len(_step_obj.context.stash.resource_list)
#     elif action_type == "sum":
#         # WARNING: Variable expansion & Interpolation might effect this result.
#         _step_obj.context.stash = sum([1 if type(b) is str else b for b in [resource.config.get('count', 1) for resource in _step_obj.context.stash.resource_list]])
#     else:
#         AssertionError("Invalid action_type in the scenario: {}".format(action_type))
#
#
# @then(u'I expect the result is {operator:ANY} than {number:d}')
# def i_expect_the_result_is_operator_than_number(_step_obj, operator, number):
#     value = int(_step_obj.context.stash)
#
#     if operator == "more":
#         assert value > number, "{} is not more than {}".format(value, number)
#     elif operator == "more and equal":
#         assert value >= number, "{} is not more and equal than {}".format(value, number)
#     elif operator == "less":
#         assert value < number, "{} is not less than {}".format(value, number)
#     elif operator == "less and equal":
#         assert value <= number, "{} is not less and equal than {}".format(value, number)
#     else:
#         AssertionError('Invalid operator: {}'.format(operator))
#
#
# @when(u'it contain {something:ANY}')
# @when(u'it contains {something:ANY}')
# @then(u'it must contain {something:ANY}')
# def it_condition_contain_something(_step_obj, something,
#                                    propertylist=TerraformPropertyList, resourcelist=TerraformResourceList):
#
#     if something in resource_name.keys():
#         something = resource_name[something]
#
#     step_can_skip = step_condition(_step_obj) in ["given", "when"]
#
#     if _step_obj.context.stash.__class__ is propertylist:
#         for prop in _step_obj.context.stash.properties:
#             value = parse_hcl_value(prop.property_value, world.config.terraform.terraform_config)
#
#             if value is not None:
#                 assert (value == something or something.lower() in value), \
#                     '{} property in {} can not be found in {} ({}). It is set to {} instead'.format(something,
#                                                                                                     prop.property_name,
#                                                                                                     prop.resource_name,
#                                                                                                     prop.resource_type,
#                                                                                                     value)
#             else:
#                 write_stdout(level='WARNING',
#                              message='Can not get value of {} in {}/{}. '
#                                      'Might be set by an unknown source (module, etc. )\n'
#                                      'Value : {}'.format(something,
#                                                          prop.property_name,
#                                                          prop.resource_type,
#                                                          prop.property_value))
#                 _step_obj.state = 'skipped'
#
#     elif _step_obj.context.stash.__class__ is resourcelist:
#         if step_can_skip is False:
#             _step_obj.context.stash.should_have_properties(something)
#             _step_obj.context.stash = _step_obj.context.stash.find_property(something)
#             assert _step_obj.context.stash.properties, \
#                 'No defined property/value found for {}.'.format(something)
#             _step_obj.context.stash = step_obj.context.stash.properties
#         else:
#             try:
#                 step_obj.context.stash.should_have_properties(something)
#                 number_of_resources = len(step_obj.context.stash.resource_list)
#                 step_obj.context.stash = step_obj.context.stash.find_property(something)
#                 if step_obj.context.stash:
#                     if number_of_resources > len(step_obj.context.stash.properties):
#                         write_stdout(level='INFO',
#                                      message='Some of the resources does not have {} property defined within.\n'
#                                              'Removed {} resource (out of {}) from the test scope.\n'
#                                              '\n'.format(something,
#                                                          (number_of_resources-len(step_obj.context.stash.properties)),
#                                                          number_of_resources,
#                                                          ))
#             except Exception as e:
#                 number_of_resources = len(step_obj.context.stash.resource_list)
#                 step_obj.context.stash = step_obj.context.stash.find_property(something)
#                 if step_obj.context.stash:
#                     write_stdout(level='INFO',
#                                  message='Some of the resources does not have {} property defined within.\n'
#                                          'Removed {} resource (out of {}) from the test scope.\n\n'
#                                          'Due to : \n'
#                                          '{}'.format(something,
#                                                      (number_of_resources-len(step_obj.context.stash.properties)),
#                                                      number_of_resources,
#                                                      str(e)))
#                 else:
#                     skip_step(step_obj,
#                               resource=something,
#                               message='Can not find {resource} property in any resource.')
#
#     elif step_obj.context.stash.__class__ is dict:
#         if something in step_obj.context.stash:
#             step_obj.context.stash = step_obj.context.stash[something]
#         else:
#             if step_can_skip:
#                 skip_step(step_obj,
#                           resource=something,
#                           message='Can not find {resource} resource in terraform files.')
#             else:
#                 assert False, '{} does not exist.'.format(something)
#
#
# @then(u'encryption is enabled')
# @then(u'encryption must be enabled')
# def encryption_is_enabled(step_obj):
#     prop = encryption_property[step_obj.context.resource_type]
#     step_obj.context.stash.property(prop).should_equal(True)
#
#
# @then(u'its value {condition:ANY} match the "{search_regex}" regex')
# def its_value_condition_match_the_search_regex_regex(step_obj, condition, search_regex):
#     regex = r'{}'.format(search_regex)
#
#     if step_obj.context.stash.__class__ is str:
#         matches = re.match(regex, step_obj.context.stash)
#
#         if condition == 'must':
#             assert matches is not None, \
#                 '{} {} tests failed on {} regex: {}'.format(step_obj.context.name,
#                                                             step_obj.context.type,
#                                                             regex,
#                                                             step_obj.context.stash)
#         elif condition == "must not":
#             assert matches is None, \
#                 '{} {} tests failed on {} regex: {}'.format(step_obj.context.name,
#                                                             step_obj.context.type,
#                                                             regex,
#                                                             step_obj.context.stash)
#     else:
#         normalise_tag_values(step_obj.context.stash)
#
#         for prop in step_obj.context.stash.properties:
#             if type(prop.property_value) is str:
#                 prop.property_value = [prop.property_value]
#             elif type(prop.property_value) is dict:
#                 prop.property_value = prop.property_value.values()
#
#             for value in prop.property_value:
#                 matches = re.match(regex, value)
#
#                 if condition == 'must':
#                     assert matches is not None, \
#                         '{} property in {} does not match with {} regex. It is set to {} instead.' \
#                         ''.format(prop.property_name,
#                                   prop.resource_name,
#                                   search_regex,
#                                   value)
#                 elif condition == 'must not':
#                     assert matches is not None, \
#                         '{} property in {} does not match with {} regex. It is set to {} instead.' \
#                         ''.format(prop.property_name,
#                                   prop.resource_name,
#                                   search_regex,
#                                   value)
#
#
# @step(u'its value must be set by a variable')
# def its_value_must_be_set_by_a_variable(step_obj):
#     step_obj.context.stash.property(step_obj.context.search_value).should_match_regex(r'\${var.(.*)}')
