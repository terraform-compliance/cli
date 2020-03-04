# -*- coding: utf-8 -*-

from radish import world, given, when, then, step
from terraform_compliance.steps import property_match_list
from terraform_compliance.common.helper import convert_resource_type, find_root_by_key, seek_key_in_dict
from terraform_compliance.common.helper import search_regex_in_list, seek_regex_key_in_dict_values, jsonify, Null, EmptyStash
from terraform_compliance.common.helper import get_resource_name_from_stash, get_resource_address_list_from_stash
from terraform_compliance.common.helper import remove_mounted_resources, search_regex_in_list, seek_value_in_dict
from terraform_compliance.extensions.security_groups import SecurityGroup
from terraform_compliance.extensions.ext_radish_bdd import skip_step
from terraform_compliance.extensions.ext_radish_bdd import custom_type_any
from terraform_compliance.extensions.ext_radish_bdd import custom_type_condition
from terraform_compliance.extensions.ext_radish_bdd import custom_type_section
from terraform_compliance.extensions.ext_radish_bdd import custom_type_prop
import re
from terraform_compliance.common.exceptions import Failure, TerraformComplianceNotImplemented
from terraform_compliance.common.exceptions import TerraformComplianceInternalFailure
from terraform_compliance.common.error_handling import Error
from terraform_compliance.main import Step
from terraform_compliance.common.defaults import Defaults
from terraform_compliance.common.bdd_tags import look_for_bdd_tags

# TODO: Figure out how the IAM policies/statements shown in the plan.out
# TODO: Implement an IAM Compliance via https://github.com/Netflix-Skunkworks/policyuniverse

types_list = ['resource', 'variable', 'provider', 'data', 'resource that supports tags']


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
                          'output', 'outputs',
                          'provider', 'providers',
                          'data', 'datas']), \
        '{} configuration type does not exist or not implemented yet. ' \
        'Use resource(s), provider(s), variable(s), output(s) or data(s) instead.'.format(type_name)

    if type_name.endswith('s'):
        type_name = type_name[:-1]

    # Process the tags
    _step_obj = look_for_bdd_tags(_step_obj)

    if name in ('a resource', 'any resource', 'resources'):
        _step_obj.context.type = type_name
        _step_obj.context.name = name
        _step_obj.context.stash = [obj for key, obj in _terraform_config.config.terraform.resources_raw.items()]
        _step_obj.context.addresses = get_resource_address_list_from_stash(_step_obj.context.stash)
        _step_obj.context.property_name = type_name
        return True

    elif name in ('an output', 'any output', 'outputs'):
        _step_obj.context.type = 'output'
        _step_obj.context.name = name
        _step_obj.context.stash = [obj for key, obj in _terraform_config.config.terraform.configuration['outputs'].items()]
        _step_obj.context.addresses = get_resource_address_list_from_stash(_terraform_config.config.terraform.configuration['outputs'])
        _step_obj.context.property_name = 'output'
        return True

    elif name in ('a variable', 'any variable', 'variables'):
        _step_obj.context.type = 'variable'
        _step_obj.context.name = name
        _step_obj.context.stash = [obj for key, obj in _terraform_config.config.terraform.configuration['variables'].items()]
        _step_obj.context.addresses = 'variable'
        _step_obj.context.property_name = 'variable'
        return True

    elif name == 'resource that supports tags':
        resource_types_supports_tags = find_root_by_key(_terraform_config.config.terraform.resources_raw,
                                                        'tags',
                                                        return_key='type')
        resource_list = []
        for resource_type in resource_types_supports_tags:
            # Issue-168: Mounted resources causes problem on recursive searching for resources that supports tags
            #            We are removing all mounted resources here for future steps, since we don't need them for
            #            tags checking.
            found_resources = remove_mounted_resources(_terraform_config.config.terraform.find_resources_by_type(resource_type))
            resource_list.extend(found_resources)

        if resource_list:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = resource_list
            _step_obj.context.addresses = get_resource_address_list_from_stash(resource_list)
            _step_obj.context.property_name = type_name
            return True

    elif type_name == 'resource':
        name = convert_resource_type(name)
        resource_list = _terraform_config.config.terraform.find_resources_by_type(name)

        if resource_list:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = resource_list
            _step_obj.context.addresses = get_resource_address_list_from_stash(resource_list)
            _step_obj.context.property_name = type_name
            return True

    elif type_name == 'variable':
        found_variable = _terraform_config.config.terraform.variables.get(name, None)

        if found_variable:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = found_variable
            _step_obj.context.addresses = name
            _step_obj.context.property_name = type_name
            return True

    elif type_name == 'output':
        found_output = _terraform_config.config.terraform.outputs.get(name, None)

        if found_output:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = found_output
            _step_obj.context.addresses = name
            _step_obj.context.property_name = type_name
            return True

    elif type_name == 'provider':
        found_provider = _terraform_config.config.terraform.get_providers_from_configuration(name)

        if found_provider:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = found_provider
            _step_obj.context.addresses = name
            _step_obj.context.address = name
            _step_obj.context.property_name = type_name
            return True

    elif type_name == 'data':
        name = convert_resource_type(name)
        data_list = _terraform_config.config.terraform.find_data_by_type(name)

        if data_list:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = data_list
            _step_obj.context.addresses = name
            _step_obj.context.address = name
            _step_obj.context.property_name = type_name
            return True

    skip_step(_step_obj, name)


@when(u'its {key:PROPERTY} is {value:PROPERTY}')
@when(u'its {key:PROPERTY} has {value:PROPERTY}')
@when(u'its {key:PROPERTY} includes {value:PROPERTY}')
@when(u'its {key:PROPERTY} contains {value:PROPERTY}')
@when(u'its {key:PROPERTY} includes "{value:ANY}"')
def its_key_is_value(_step_obj, key, value):
    orig_key = key
    if key == 'reference':
        key = Defaults.address_pointer

    found_list = []
    for obj in _step_obj.context.stash:
        object_key = obj.get('values', {})
        if isinstance(object_key, list):
            object_keys = []
            for object_key_element in object_key:
                if isinstance(object_key_element, dict):
                    filtered_key = object_key_element.get(key)
                    if isinstance(filtered_key, str) and filtered_key.lower() == value.lower():
                        found_list.append(object_key_element)
                else:
                    object_keys.append(object_key_element.get(key, Null))

            object_key = [keys for keys in object_keys if keys is not Null]
        else:
            object_key = object_key.get(key, Null)

        if object_key is Null:
            object_key = obj.get(key, Null)

        if isinstance(object_key, str):
            if "[" in object_key:
                object_key = object_key.split('[')[0]

            if object_key.lower() == value.lower():
                found_list.append(obj)

        elif isinstance(object_key, (int, bool)) and object_key == value:
            found_list.append(obj)

        elif isinstance(object_key, list) and value in object_key:
            found_list.append(obj)

        elif isinstance(object_key, dict) and (value in object_key.keys()):
            found_list.append(obj)

    if found_list != []:
        _step_obj.context.stash = found_list
        _step_obj.context.addresses = get_resource_address_list_from_stash(found_list)
    else:
        skip_step(_step_obj, message='Can not find {} {} in {}.'.format(value, orig_key,
                                                                        ', '.join(_step_obj.context.addresses)))


@when(u'its {key:PROPERTY} is not {value:PROPERTY}')
@when(u'its {key:PROPERTY} has not {value:PROPERTY}')
@when(u'its {key:PROPERTY} does not include {value:PROPERTY}')
@when(u'its {key:PROPERTY} does not contain {value:PROPERTY}')
@when(u'its {key:PROPERTY} does not include "{value:ANY}"')
def its_key_is_not_value(_step_obj, key, value):
    orig_key = key
    if key == 'reference':
        key = Defaults.address_pointer

    key = str(key).lower()
    found_list = []
    for obj in _step_obj.context.stash:
        object_key = obj.get(key, Null)

        if object_key is Null:
            object_key = obj.get('values', {})
            if isinstance(object_key, list):
                object_keys = []
                for object_key_element in object_key:
                    if object_key_element.get(key, Null) != value:
                        object_keys.append(object_key_element.get(key, Null))

                object_key = [keys for keys in object_keys if keys is not Null]
            else:
                object_key = object_key.get(key, Null)

        if isinstance(object_key, str):
            if "[" in object_key:
                object_key = object_key.split('[')[0]

            if object_key != value:
                found_list.append(obj)

        elif isinstance(object_key, (int, bool)) and object_key != value:
            found_list.append(obj)

        elif isinstance(object_key, list) and value not in object_key:
            found_list.append(obj)

        elif isinstance(object_key, dict) and (value not in object_key.keys()):
            found_list.append(obj)

    if found_list != []:
        _step_obj.context.stash = found_list
        _step_obj.context.addresses = get_resource_address_list_from_stash(found_list)
    else:
        skip_step(_step_obj, message='Found {} {} in {}.'.format(value, orig_key,
                                                                 ', '.join(_step_obj.context.addresses)))


@when(u'it contain {something:ANY}')
@when(u'they have {something:ANY}')
@when(u'it has {something:ANY}')
@when(u'it contains {something:ANY}')
@then(u'it must contain {something:ANY}')
def it_condition_contain_something(_step_obj, something, inherited_values=Null):
    prop_list = []

    _step_obj.context.stash = inherited_values if inherited_values is not Null else _step_obj.context.stash

    if _step_obj.context.type in ('resource', 'data'):
        for resource in _step_obj.context.stash:
            if not isinstance(resource, dict) \
                    or 'values' not in resource \
                    or 'address' not in resource \
                    or 'type' not in resource:
                resource = {'values': resource,
                            'address': resource,
                            'type': _step_obj.context.name}

            values = resource.get('values', resource.get('expressions', {}))
            if not values:
                values = seek_key_in_dict(resource, something)

            found_value = Null
            found_key = Null
            if isinstance(values, dict):
                found_key = values.get(something, seek_key_in_dict(values, something))
                if not isinstance(found_key, list):
                    found_key = [{something: found_key}]

                if len(found_key):
                    found_key = found_key[0] if len(found_key) == 1 and something in found_key[0] else found_key

                    if isinstance(found_key, dict):
                        found_value = jsonify(found_key.get(something, found_key))
                    else:
                        found_value = found_key
            elif isinstance(values, list):
                found_value = []

                for value in values:

                    if isinstance(value, dict):
                        # First search in the keys
                        found_key = seek_key_in_dict(value, something)

                        # Then search in the values with 'key'
                        if not found_key:
                            found_key = seek_regex_key_in_dict_values(value, 'key', something)

                            if found_key:
                                found_key = found_key[0]
                                found_value = value.get('value')
                                break
                    elif isinstance(value, list):
                        found_key, found_value = it_condition_contain_something(_step_obj, something, value)

                    if found_key is not Null and len(found_key):
                        found_key = found_key[0] if len(found_key) == 1 else found_key

                        if isinstance(found_key, dict):
                            found_value.append(jsonify(found_key.get(something, found_key)))

            if isinstance(found_value, dict) and 'constant_value' in found_value:
                found_value = found_value['constant_value']

            if found_value is not Null and found_value != [] and found_value != '' and found_value != {}:
                prop_list.append({'address': resource['address'],
                                  'values': found_value,
                                  'type': _step_obj.context.name})

            elif 'must' in _step_obj.context_sensitive_sentence:
                Error(_step_obj, '{} ({}) does not have {} property.'.format(resource['address'],
                                                                             resource.get('type', ''),
                                                                             something))

        if prop_list:
            _step_obj.context.stash = prop_list
            _step_obj.context.property_name = something
            return something, prop_list

        if _step_obj.state != Step.State.FAILED:
            skip_step(_step_obj,
                      resource=_step_obj.context.name,
                      message='Can not find any {} property for {} resource in '
                              'terraform plan.'.format(something, _step_obj.context.name))

    elif _step_obj.context.type == 'provider':
        for provider_data in _step_obj.context.stash:
            values = seek_key_in_dict(provider_data, something)

            if values:
                _step_obj.context.stash = values
                _step_obj.context.property_name = something
                _step_obj.context.address = '{}.{}'.format(provider_data.get('name', _step_obj.context.addresses),
                                                           provider_data.get('alias', "\b"))
                return True
            elif 'must' in _step_obj.context_sensitive_sentence:
                Error(_step_obj, '{} {} does not have {} property.'.format(_step_obj.context.addresses,
                                                                           _step_obj.context.type,
                                                                           something))
        if 'must' in _step_obj.context_sensitive_sentence:
            Error(_step_obj, '{} {} does not have {} property.'.format(_step_obj.context.addresses,
                                                                       _step_obj.context.type,
                                                                       something))
    if _step_obj.state != Step.State.FAILED:
        skip_step(_step_obj,
                  resource=_step_obj.context.name,
                  message='Skipping the step since {} type does not have {} property.'.format(_step_obj.context.type,
                                                                                              something))


@then(u'{something:ANY} is be enabled')
@then(u'{something:ANY} must be enabled')
def property_is_enabled(_step_obj, something):
    for resource in _step_obj.context.stash:
        if isinstance(resource, dict):
            if something in property_match_list:
                something = property_match_list[something].get(resource['type'], something)

            property_value = seek_key_in_dict(resource.get('values', {}), something)

            if len(property_value):
                property_value = property_value[0]

                if isinstance(property_value, dict):
                    property_value = property_value.get(something, Null)

            if not property_value:
                Error(_step_obj, 'Resource {} does not have {} property enabled '
                                 '({}={}).'.format(resource.get('address', "resource"),
                                                   something,
                                                   something,
                                                   property_value))
    return True


@then(u'it {condition:ANY} have {proto:ANY} protocol and port {port} for {cidr:ANY}')
def it_condition_have_proto_protocol_and_port_port_for_cidr(_step_obj, condition, proto, port, cidr):
    searching_for=dict(port=port, protocol=proto, cidr_blocks=cidr)

    for sg in _step_obj.context.stash:
        if sg['type'] != 'aws_security_group':
            raise TerraformComplianceInternalFailure('This method can only be used for aws_security_group resources '
                                                     'for now. You tried to used it on {}'.format(sg['type']))

        sg_obj = SecurityGroup(searching_for, sg['values'], address=sg['address'])
        if condition == 'must only':
            sg_obj.must_only_have()
        elif condition == 'must':
            sg_obj.must_have()
        elif condition == 'must not':
            sg_obj.must_not_have()
        else:
            raise TerraformComplianceInternalFailure('You can only use "must have", "must not have" and "must only have"'
                                                     'conditions on this step for now.'
                                                     'You tried to use "{}"'.format(condition))
        result, message = sg_obj.validate()

        if result is False:
            Error(_step_obj, message)

    return True


@when(u'I {action_type:ANY} it')
@when(u'I {action_type:ANY} them')
@when(u'I {action_type:ANY} the value')
def i_action_them(_step_obj, action_type):
    if action_type == "count":
        # WARNING: Only case where we set stash as a dictionary, instead of a list.
        if isinstance(_step_obj.context.stash, list):

            # This means we are directly started counting without drilling down any property
            # Thus, our target for the count is stash itself.
            if _step_obj.context.property_name in types_list:
                _step_obj.context.stash = dict(values=len(_step_obj.context.stash))

            else:
                if isinstance(_step_obj.context.stash[0], dict):
                    if _step_obj.context.stash[0].get('values'):
                        _step_obj.context.stash = seek_key_in_dict(_step_obj.context.stash, 'values')
                        count = 0
                        for result in _step_obj.context.stash:
                            count += len(result.get('values', {})) if result.get('values') else 1

                        _step_obj.context.stash = dict(values=count)

                else:
                    _step_obj.context.stash = dict(values=len(_step_obj.context.stash))
    else:
        raise TerraformComplianceNotImplemented('Invalid action_type in the scenario: {}'.format(action_type))


@then(u'its value must be {operator:ANY} than {number:d}')
@then(u'I expect the result is {operator:ANY} than {number:d}')
@then(u'its value must be {operator:ANY} to {number:d}')
@then(u'I expect the result is {operator:ANY} to {number:d}')
def i_expect_the_result_is_operator_than_number(_step_obj, operator, number, _stash=EmptyStash):

    def fail(assertion, message):
        try:
            assert assertion, 'Failed'
        except AssertionError as e:
            Error(_step_obj, 'for {} on {}. {}.'.format(_step_obj.context.address,
                                                        _step_obj.context.property_name,
                                                        message))

    values = _step_obj.context.stash if _stash is EmptyStash else _stash

    if isinstance(values, list):
        for value_set in values:
            i_expect_the_result_is_operator_than_number(_step_obj, operator, number, _stash=value_set)

    elif isinstance(values, dict):
        _step_obj.context.property_name = values.get('type', _step_obj.context.property_name)
        _step_obj.context.address = values.get('address', _step_obj.context.addresses)

        if isinstance(_step_obj.context.address, list) and len(_step_obj.context.address) == 1:
            _step_obj.context.address = _step_obj.context.address[0]

        i_expect_the_result_is_operator_than_number(_step_obj, operator, number, values.get('values', Null))

    elif isinstance(values, (int, str)):
        values = int(values)
        if operator in ('more', 'greater', 'bigger'):
            fail(values > number, '{} is not more than {}'.format(values, number))
        elif operator in ('more and equal', 'greater and equal', 'bigger and equal'):
            fail(values >= number, '{} is not more and equal than {}'.format(values, number))
        elif operator in ('less', 'lesser', 'smaller'):
            fail(values < number, '{} is not less than {}'.format(values, number))
        elif operator in ('less and equal', 'lesser and equal', 'smaller and equal'):
            fail(values <= number, '{} is not less and equal than {}'.format(values, number))
        elif operator in ('equal',):
            fail(values == number, '{} is not equal to {}'.format(values, number))
        else:
            raise TerraformComplianceNotImplemented('Invalid operator: {}'.format(operator))

    elif isinstance(values, Null):
        raise TerraformComplianceNotImplemented('Null/Empty value found on {}'.format(_step_obj.context.type))


@then(u'its value {condition:ANY} match the "{search_regex}" regex')
def its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, _stash=EmptyStash):
    def fail(condition, name=None):
        text = 'matches' if condition == 'must not' else 'does not match'
        name = name if (name is not None or name is not False) else _step_obj.context.name
        pattern = 'Null/None' if regex == '\x00' else regex
        Error(_step_obj, '{} property in {} {} {} with {} regex. '
                         'It is set to {}.'.format(_step_obj.context.property_name,
                                                   name,
                                                   _step_obj.context.type,
                                                   text,
                                                   pattern,
                                                   values))

    regex = r'{}'.format(search_regex)
    values = _step_obj.context.stash if _stash is EmptyStash else _stash

    if isinstance(values, (str, int, bool)) or values is None:
        matches = re.match(regex, str(values), flags=re.IGNORECASE)

        if (condition == 'must' and matches is None) or (condition == "must not" and matches is not None):
            _stash = get_resource_name_from_stash(_step_obj.context.stash, _stash, _step_obj.context.address)
            fail(condition, name=_stash.get('address'))

    elif isinstance(values, list):
        for value in values:
            its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, value)

    elif isinstance(values, dict):
        if not hasattr(_step_obj.context, 'address'):
            _step_obj.context.address = None

        _step_obj.context.address = values.get('address', _step_obj.context.address)

        if 'values' in values:
            if values['values'] is None and regex == '\x00' and condition == 'must not':
                values = values['values']
                fail(condition, name=_stash.get('address'))
            else:
                its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, values.get('values'))

        else:
            for key, value in values.items():
                its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, value)


@then(u'its value {condition:ANY} be {match:ANY}')
def its_value_condition_equal(_step_obj, condition, match, _stash=EmptyStash):
    its_value_condition_match_the_search_regex_regex(_step_obj, condition, "^" + re.escape(match) + "$", _stash)


@then(u'its value {condition:ANY} contain {value:ANY}')
def its_value_condition_contain(_step_obj, condition, value, _stash=EmptyStash):
    if condition not in ('must', 'must not'):
        raise TerraformComplianceNotImplemented('Condition should be one of: `must`, `must not`')

    values = _step_obj.context.stash if _stash is EmptyStash else _stash
    # TODO: Update here for checking values in a list or dict.

    if isinstance(values, list):
        for elem in values:
            values = its_value_condition_contain(_step_obj, condition, value, elem)

    if isinstance(values, (int, bool, str, float)):
        values = dict(values=values,
                      address=_step_obj.context.address if hasattr(_step_obj.context, 'address') else _step_obj.context.addresses)

    found_values = seek_value_in_dict(value, values)
    condition = condition == 'must'

    if condition and not found_values:
        if isinstance(values, list):
            objects = []
            for elem in values:
                objects.append(elem.get('address', '???'))
            objects = ', '.join(objects)
        else:
            objects = values.get('address')

        Error(_step_obj, '{} could not found in {}.'.format(value, objects))

    elif not condition and found_values:
        Error(_step_obj, '{} found in {}.'.format(value,
                                                  get_resource_name_from_stash(found_values).get('address')))

    return values


def _its_value_condition_contain(_step_obj, condition, value, values):
    if isinstance(values, list):
        values = [str(v) for v in values]
        _fail_text = 'did not contain' if condition == 'must' else 'contains'
        fail_message = '{} property in {} {} {}, it is set to {}'.format(
            _step_obj.context.property_name,
            _step_obj.context.name,
            _fail_text,
            value,
            values,
        )
        if condition == 'must':
            assert value in values, fail_message
        else:
            assert value not in values, fail_message
    else:
        raise TerraformComplianceInternalFailure('Can only check that if list contains value')


@then(u'the scenario fails')
@then(u'the scenario should fail')
@then(u'the scenario must fail')
@then(u'it fails')
@then(u'it should fail')
@then(u'it must fail')
def it_fails(_step_obj):
    Error(_step_obj, 'Forcefully failing the scenario on {} ({}) {}'.format(_step_obj.context.name,
                                                                            ', '.join(_step_obj.context.addresses),
                                                                            _step_obj.context.type))


@then(u'its value {condition:ANY} be null')
def its_value_condition_be_null(_step_obj, condition):
    its_value_condition_match_the_search_regex_regex(_step_obj, condition, u'\x00')
    its_value_condition_match_the_search_regex_regex(_step_obj, condition, u'^$')
    its_value_condition_match_the_search_regex_regex(_step_obj, condition, u'^null$')


@then(u'it must have "{reference_address}" referenced')
def it_must_have_reference_address_referenced(_step_obj, reference_address):
    if _step_obj.context.stash:
        for resource in _step_obj.context.stash:
            if isinstance(resource, dict):
                if Defaults.address_pointer in resource and search_regex_in_list(reference_address,
                                                                                 resource[Defaults.address_pointer]):
                    return True
            else:
                raise TerraformComplianceInternalFailure('Unexpected resource structure: {}'.format(resource))

            Error(_step_obj, '{} is not referenced within {}.'.format(reference_address, resource.get('address')))
    else:
        Error(_step_obj, 'No entities found for this step to process. Check your filtering steps in this scenario.')


@then('its {key:ANY} {condition:ANY} be {value:ANY}')
@then('its {key:ANY} property {condition:ANY} be {value:ANY}')
@then('its {key:ANY} key {condition:ANY} be {value:ANY}')
def its_key_condition_be_value(_step_obj, key, condition, value, stash=Null, depth=0):
    if condition not in ('must', 'must not'):
        raise TerraformComplianceNotImplemented('This step only accepts "must" and "must not" as a condition.')

    if stash is Null:
        stash = _step_obj.context.stash

    if not stash or stash is Null:
        Error(_step_obj, 'No entities found for this step to process. Check your filtering steps in this scenario.')
        return False

    found_values = []
    for entity in stash:
        if isinstance(entity, dict):
            found_values.extend(seek_regex_key_in_dict_values(entity, key, value))
        elif isinstance(entity, list):
            for element in entity:
                found_values.extend(its_key_condition_be_value(_step_obj, key, condition, element, entity, depth+1))
        elif isinstance(entity ,(str, int, bool)) and (str(entity).lower == key.lower or str(entity) == value.lower):
            found_values.append(entity)

    # Return the values to the parent call.
    if depth > 0:
        return found_values

    condition = condition == 'must'
    found_values = [values for values in found_values if values is not None]

    obj_address = _step_obj.context.name
    if hasattr(_step_obj.context, 'address'):
        obj_address = _step_obj.context.address
    elif hasattr(_step_obj.context, 'addresses'):
        obj_address = ', '.join(_step_obj.context.addresses)

    if found_values and not condition:
        Error(_step_obj, 'Found {}({}) in {} property of {}.'.format(value, ', '.join(found_values), key, obj_address))
    elif not found_values and condition:
        Error(_step_obj, 'Can not find {} in {} property of {}.'.format(value, key, obj_address))

    return True


@then('I flatten all values found')
def i_flatten_everything_found(_step_obj):
    flattened_list = []
    addresses_flattened = []
    for each in _step_obj.context.stash:
        flattened_list.append(each.get('values', each))
        addresses_flattened.append(each.get('address', each))

    if flattened_list:
        _step_obj.context.stash = {
            'address': ', '.join(addresses_flattened),
            'values': flattened_list
        }

    return flattened_list
