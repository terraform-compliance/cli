# -*- coding: utf-8 -*-

from radish import world, given, when, then, step
from terraform_compliance.steps import property_match_list
from terraform_compliance.common.helper import check_sg_rules, convert_resource_type, find_root_by_key, seek_key_in_dict
from terraform_compliance.common.helper import seek_regex_key_in_dict_values, jsonify, Null, EmptyStash
from terraform_compliance.common.helper import get_resource_name_from_stash
from terraform_compliance.extensions.ext_radish_bdd import skip_step
from terraform_compliance.extensions.ext_radish_bdd import custom_type_any, custom_type_condition, custom_type_section
import re
from terraform_compliance.common.exceptions import Failure, TerraformComplianceNotImplemented
from terraform_compliance.common.exceptions import TerraformComplianceInternalFailure


# TODO: Figure out how the IAM policies/statements shown in the plan.out
# TODO: Implement an IAM Compliance via https://github.com/Netflix-Skunkworks/policyuniverse



# def i have_name_defined(_step_obj, name, _terraform_config=world):
#     pass

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
    assert (type_name in ['resource', 'resources',
                          'variable', 'variables',
                          'provider', 'providers',
                          'data', 'datas']), \
        '{} configuration type does not exist or not implemented yet. ' \
        'Use resource(s), provider(s), variable(s) or data(s) instead.'.format(type_name)

    if type_name.endswith('s'):
        type_name = type_name[:-1]

    if name == 'resource that supports tags':
        resource_types_supports_tags = find_root_by_key(_terraform_config.config.terraform.resources_raw,
                                                        'tags',
                                                        return_key='type')
        resource_list = []
        for resource_type in resource_types_supports_tags:
            resource_list.extend(_terraform_config.config.terraform.find_resources_by_type(resource_type))

        if resource_list:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = resource_list
            return True

    elif type_name == 'resource':
        name = convert_resource_type(name)
        resource_list = _terraform_config.config.terraform.find_resources_by_type(name)

        if resource_list:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = resource_list
            return True

    elif type_name == 'variable':
        found_variable = _terraform_config.config.terraform.variables.get(name, None)

        if found_variable:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = found_variable
            return True

    elif type_name == 'provider':
        found_provider = _terraform_config.config.terraform.configuration.get('providers', {}).get(name, None)

        if found_provider:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = found_provider
            return True

    elif type_name == 'data':
        name = convert_resource_type(name)
        data_list = _terraform_config.config.terraform.find_data_by_type(name)

        if data_list:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = data_list
            return True

    skip_step(_step_obj, name)


@when(u'its {key:ANY} is {value:ANY}')
@when(u'its {key:ANY} has {value:ANY}')
@when(u'its {key:ANY} includes {value:ANY}')
@when(u'its {key:ANY} consists {value:ANY}')
def its_key_is_value(_step_obj, key, value):
    search_key = str(key).lower()
    found_list = []
    for obj in _step_obj.context.stash:
        object_key = obj.get(key, Null)

        if object_key is Null:
            object_key = obj.get('values', {}).get(key, Null)

        if type(object_key) is str:
            if "[" in object_key:
                object_key = object_key.split('[')[0]

            if object_key == value:
                found_list.append(obj)

        elif type(object_key) in (int, bool) and object_key == value:
            found_list.append(obj)

        elif type(object_key) is list and value in object_key:
            found_list.append(obj)

        elif type(object_key) is dict and (value in object_key.keys()):
            found_list.append(obj)

    if found_list is not []:
        _step_obj.context.stash = found_list
    else:
        skip_step(_step_obj, value)


@when(u'it contain {something:ANY}')
@when(u'they have {something:ANY}')
@when(u'it has {something:ANY}')
@when(u'it contains {something:ANY}')
@then(u'it must contain {something:ANY}')
def it_condition_contain_something(_step_obj, something):
    prop_list = []

    if _step_obj.context.type in ('resource', 'data'):
        for resource in _step_obj.context.stash:
            if type(resource) is not dict:
                resource = {'values': resource,
                            'address': resource,
                            'type': _step_obj.context.name}

            values = resource.get('values', resource.get('expressions', {}))

            found_value = Null
            found_key = Null
            if type(values) is dict:
                found_key = values.get(something, seek_key_in_dict(values, something))
                if type(found_key) is not list:
                    found_key = [{something: found_key}]

                if len(found_key):
                    found_key = found_key[0] if len(found_key) == 1 else found_key

                    if type(found_key) is dict:
                        found_value = jsonify(found_key.get(something, found_key))
                    else:
                        found_value = found_key
            elif type(values) is list:
                found_value = []

                for value in values:

                    if type(value) is dict:
                        # First search in the keys
                        found_key = seek_key_in_dict(value, something)

                        # Then search in the values with 'key'
                        if not found_key:
                            found_key = seek_regex_key_in_dict_values(value, 'key', something)

                            if found_key:
                                found_key = found_key[0]
                                found_value = value.get('value')
                                break

                    if found_key is not Null and len(found_key):
                        found_key = found_key[0] if len(found_key) == 1 else found_key

                        if type(found_key) is dict:
                            found_value.append(jsonify(found_key.get(something, found_key)))

            if type(found_value) is dict and 'constant_value' in found_value:
                found_value = found_value['constant_value']

            if found_value is not Null and found_value != [] and found_value != '' and found_value != {}:
                prop_list.append({'address': resource['address'],
                                  'values': found_value,
                                  'type': _step_obj.context.name})

            elif 'must' in _step_obj.context_sensitive_sentence:
                raise Failure('{} ({}) does not have {} property.'.format(resource['address'],
                                                                          resource.get('type', ''),
                                                                          something))

        if prop_list:
            _step_obj.context.stash = prop_list
            _step_obj.context.property_name = something
            return True

        skip_step(_step_obj,
                  resource=_step_obj.context.name,
                  message='Can not find any {} property for {} resource in '
                          'terraform plan.'.format(something, _step_obj.context.name))

    elif _step_obj.context.type == 'provider':
        values = seek_key_in_dict(_step_obj.context.stash, something)

        if values:
            _step_obj.context.stash = values
            _step_obj.context.property_name = something
            return True

    skip_step(_step_obj,
              resource=_step_obj.context.name,
              message='Skipping the step since {} type does not have {} property.'.format(_step_obj.context.type,
                                                                                          something))



@then(u'{something:ANY} is be enabled')
@then(u'{something:ANY} must be enabled')
def property_is_enabled(_step_obj, something):
    for resource in _step_obj.context.stash:
        if type(resource) is dict:
            if something in property_match_list:
                something = property_match_list[something].get(resource['type'], something)

            property_value = seek_key_in_dict(resource.get('values', {}), something)

            if len(property_value):
                property_value = property_value[0]

                if type(property_value) is dict:
                    property_value = property_value.get(something, Null)

            if not property_value:
                raise Failure('Resource {} does not have {} property enabled ({}={}).'.format(resource.get('address', "resource"),
                                                                                              something,
                                                                                              something,
                                                                                              property_value))
    return True


@then(u'it must {condition:ANY} have {proto:ANY} protocol and port {port} for {cidr:ANY}')
def it_condition_have_proto_protocol_and_port_port_for_cidr(_step_obj, condition, proto, port, cidr):
    proto = str(proto)
    cidr = str(cidr)

    # Set to True only if the condition is 'only'
    condition = condition == 'only'

    # In case we have a range
    if '-' in port:
        if condition:
            raise Failure('"must only" scenario cases must be used either with individual port '
                          'or multiple ports separated with comma.')

        from_port, to_port = port.split('-')
        ports = [from_port, to_port]

    # In case we have comma delimited ports
    elif ',' in port:
        ports = [port for port in port.split(',')]
        from_port = min(ports)
        to_port = max(ports)

    else:
        from_port = to_port = int(port)
        ports = list(set([str(from_port), str(to_port)]))

    from_port = int(from_port) if int(from_port) > 0 else 1
    to_port = int(to_port) if int(to_port) > 0 else 1
    ports[0] = ports[0] if int(ports[0]) > 0 else '1'

    looking_for = dict(proto=proto,
                       from_port=int(from_port),
                       to_port=int(to_port),
                       ports=ports,
                       cidr=cidr)

    for security_group in _step_obj.context.stash:
        if type(security_group['values']) is list:
            for sg in security_group['values']:
                check_sg_rules(plan_data=sg, security_group=looking_for, condition=condition)

        elif type(security_group['values']) is dict:
            check_sg_rules(plan_data=security_group['values'], security_group=looking_for, condition=condition)
        else:
            raise TerraformComplianceInternalFailure('Unexpected Security Group, '
                                                     'must be either list or a dict: '
                                                     '{}'.format(security_group['values']))
    return True

@when(u'I {action_type:ANY} it')
@when(u'I {action_type:ANY} them')
@when(u'I {action_type:ANY} the value')
@then(u'I {action_type:ANY} it')
@then(u'I {action_type:ANY} them')
@then(u'I {action_type:ANY} the value')
def i_action_them(_step_obj, action_type):
    if action_type == "count":
        # WARNING: Only case where we set stash as a dictionary, instead of a list.
        if type(_step_obj.context.stash) is list:
            if type(_step_obj.context.stash[0]) is dict():
                if _step_obj.context.stash.get('values'):
                    _step_obj.context.stash = seek_key_in_dict(_step_obj.context.stash, 'values')
                    count = 0
                    for result in _step_obj.context.stash:
                        count += len(result.get('values', {})) if result.get('values') else 1

                    _step_obj.context.stash = {'values': count}
            else:
                _step_obj.context.stash = {'values': len(_step_obj.context.stash)}
    else:
        raise TerraformComplianceNotImplemented('Invalid action_type in the scenario: {}'.format(action_type))


@then(u'Its value must be {operator:ANY} than {number:d}')
@then(u'I expect the result is {operator:ANY} than {number:d}')
def i_expect_the_result_is_operator_than_number(_step_obj, operator, number, _stash=EmptyStash):
    values = _step_obj.context.stash if _stash is EmptyStash else _stash

    if type(values) is list:
        for value_set in values:
            i_expect_the_result_is_operator_than_number(_step_obj, operator, number, _stash=value_set)

    elif type(values) is dict:
        i_expect_the_result_is_operator_than_number(_step_obj, operator, number, values.get('values', Null))

    elif type(values) is int or type(values) is str:
        values = int(values)
        if operator in ("more", "greater", "bigger"):
            assert values > number, "{} is not more than {}".format(values, number)
        elif operator in ("more and equal", "greater and equal", "bigger and equal"):
            assert values >= number, "{} is not more and equal than {}".format(values, number)
        elif operator in ("less", "lesser", "smaller"):
            assert values < number, "{} is not less than {}".format(values, number)
        elif operator in ("less and equal", "lesser and equal", "smaller and equal"):
            assert values <= number, "{} is not less and equal than {}".format(values, number)
        else:
            raise TerraformComplianceNotImplemented('Invalid operator: {}'.format(operator))

    elif type(values) is Null:
        raise TerraformComplianceNotImplemented('Null/Empty value found on {}'.format(_step_obj.context.type))

@step(u'its value {condition:ANY} match the "{search_regex}" regex')
def its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, _stash=EmptyStash):
    def fail(condition, name=None):
        text = 'matches' if condition == 'must not' else 'does not match'
        name = name if (name is not None or name is not False) else _step_obj.context.name
        pattern = 'Null/None' if regex == '\x00' else regex
        raise Failure('{} property in {} {} {} with {} regex. '
                      'It is set to {}.'.format(_step_obj.context.property_name,
                                                name,
                                                _step_obj.context.type,
                                                text,
                                                pattern,
                                                values))
    regex = r'{}'.format(search_regex)
    values = _step_obj.context.stash if _stash is EmptyStash else _stash

    if type(values) in (str, int, bool) or values is None:
        matches = re.match(regex, str(values), flags=re.IGNORECASE)

        if (condition == 'must' and matches is None) or (condition == "must not" and matches is not None):
            _stash = get_resource_name_from_stash(_step_obj.context.stash, _stash)
            fail(condition, name=_stash.get('address'))

    elif type(values) is list:
        for value in values:
            its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, value)

    elif type(values) is dict:
        if 'values' in values:
            if values['values'] is None and regex == '\x00' and condition == 'must not':
                values = values['values']
                fail(condition, name=_stash.get('address'))
            else:
                its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, values.get('values'))

        else:
            for key, value in values.items():
                its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, value)

@then(u'the scenario fails')
@then(u'the scenario should fail')
@then(u'it fails')
@then(u'it should fail')
@then(u'it must fail')
def it_fails(_step_obj):
    raise Failure('Forcefully failing the scenario on {} {}'.format(_step_obj.context.name,
                                                                    _step_obj.context.type))


@then(u'its value {condition:ANY} be null')
def its_value_condition_be_null(_step_obj, condition):
    its_value_condition_match_the_search_regex_regex(_step_obj, condition, u'\x00')
    its_value_condition_match_the_search_regex_regex(_step_obj, condition, u'^$')
    its_value_condition_match_the_search_regex_regex(_step_obj, condition, u'^null$')
