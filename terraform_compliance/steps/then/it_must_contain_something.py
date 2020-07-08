# -*- coding: utf-8 -*-

from terraform_compliance.common.helper import (
    seek_key_in_dict,  # importing this purely because the unit tests require it to exist in global scope
    Null
)
from terraform_compliance.common.error_handling import Error


def it_must_contain_something(_step_obj, something, inherited_values=Null):
    match = _step_obj.context.match
    seek_key_in_dict, seek_regex_key_in_dict_values = match.seek_key_in_dict, match.seek_regex_key_in_dict_values

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

            # not going to use match.get here because the following line is an edge case
            values = resource.get('values', resource.get('expressions', {}))
            if not values:
                values = seek_key_in_dict(resource, something)

            found_value = Null
            found_key = Null
            if isinstance(values, dict):
                found_key = match.get(values, something, seek_key_in_dict(values, something))
                if not isinstance(found_key, list):
                    found_key = [{something: found_key}]

                if len(found_key):
                    found_key = found_key[0] if len(found_key) == 1 and something in found_key[0] else found_key

                    if isinstance(found_key, dict):
                        found_value = match.get(found_key, something, found_key)
                        found_value = found_value if found_value not in ([], '') else found_key
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
                                # not going to use match.get here because the following line is an edge case
                                found_value.extend(value.get('value'))
                                break
                    elif isinstance(value, list):
                        found_key, temp_found_value = it_must_contain_something(_step_obj, something, value)
                        found_value.extend(temp_found_value)

                    elif isinstance(value, (str, bool, int, float)):
                        if match.equals(value, something):
                            found_value.append(value)

                    if found_key is not Null and len(found_key):
                        found_key = found_key[0] if len(found_key) == 1 else found_key

                        if isinstance(found_key, dict):
                            found_value.append(found_key.get(something, found_key))

            if isinstance(found_value, dict) and 'constant_value' in found_value:
                found_value = found_value['constant_value']

            if found_value not in (Null, [], '', {}):
                prop_list.append({'address': resource['address'],
                                  'values': found_value,
                                  'type': _step_obj.context.name})

            else:
                Error(_step_obj, '{} ({}) does not have {} property.'.format(resource['address'],
                                                                             resource.get('type', ''),
                                                                             something))

        if prop_list:
            _step_obj.context.stash = prop_list
            _step_obj.context.property_name = something
            return something, prop_list

    elif _step_obj.context.type == 'provider':
        _step_obj.context.stash = []
        for provider_data in _step_obj.context.stash:
            values = seek_key_in_dict(provider_data, something)

            if values:
                _step_obj.context.stash.append(values)
                _step_obj.context.property_name = something
                _step_obj.context.address = '{}.{}'.format(provider_data.get('name', _step_obj.context.addresses),
                                                           provider_data.get('alias', "\b"))
                return True
            else:
                Error(_step_obj, '{} {} does not have {} property.'.format(_step_obj.context.addresses,
                                                                           _step_obj.context.type,
                                                                           something))

        Error(_step_obj, '{} {} does not have {} property.'.format(_step_obj.context.addresses,
                                                                   _step_obj.context.type,
                                                                   something))


def it_must_not_contain_something(_step_obj, something, inherited_values=Null):
    match = _step_obj.context.match
    seek_key_in_dict, seek_regex_key_in_dict_values = match.seek_key_in_dict, match.seek_regex_key_in_dict_values

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
                found_key = match.get(values, something, seek_key_in_dict(values, something))
                if not isinstance(found_key, list):
                    found_key = [{something: found_key}]

                if len(found_key):
                    found_key = found_key[0] if len(found_key) == 1 and something in found_key[0] else found_key

                    if isinstance(found_key, dict):
                        found_value = match.get(found_key, something, found_key)
                        found_value = found_value if found_value not in ([], '') else found_key
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
                                found_value.append(value.get('value'))
                                break
                    elif isinstance(value, list):
                        found_key, temp_found_value = it_must_contain_something(_step_obj, something, value)
                        found_value.extend(temp_found_value)

                    elif isinstance(value, (str, bool, int, float)):
                        if match.equals(value, something):
                            found_value.append(value)

                    if found_key is not Null and len(found_key):
                        found_key = found_key[0] if len(found_key) == 1 else found_key

                        if isinstance(found_key, dict):
                            found_value.append(found_key.get(something, found_key))

            if isinstance(found_value, dict) and 'constant_value' in found_value:
                found_value = found_value['constant_value']

            # if found_value is not Null and found_value != [] and found_value != '' and found_value != {}:
            if found_value not in (Null, [], '', {}):
                Error(_step_obj, '{} property exists in {} ({}).'.format(something, resource['address'], resource.get('type', '')))

    elif _step_obj.context.type == 'provider':
        for provider_data in _step_obj.context.stash:
            values = seek_key_in_dict(provider_data, something)

            if values:
                Error(_step_obj, '{} {} does not have {} property.'.format(_step_obj.context.addresses,
                                                                           _step_obj.context.type,
                                                                           something))
