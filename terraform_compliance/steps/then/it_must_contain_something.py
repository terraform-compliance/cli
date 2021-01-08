# -*- coding: utf-8 -*-

from terraform_compliance.common.helper import (
    seek_key_in_dict,  # importing this purely because the unit tests require it to exist in global scope
    Null
)
from terraform_compliance.common.error_handling import Error


def it_must_contain_something(_step_obj, something, inherited_values=Null, child=False):
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

            found_values = []
            found_key = Null # this could also become a list
            resource_passed = False
            # set this to True if you get anything from the resource, don't set it to False if you get empty values as there could be other values as well
            if isinstance(values, dict):

                found_key = match.get(values, something, Null)
                if found_key is not Null:
                    found_key = [{something: found_key}]
                else:
                    found_key = seek_key_in_dict(values, something)

                for kv_pair in found_key:
                    # kv_pair must be in {something: found_key} format.
                    if not isinstance(kv_pair, dict):
                        continue # should raise exception
                    # ignore the values that correspond to Null 
                    # Following line could be problematic, how to determine if something is set to be empty or not set? Behavior is provider dependent. 
                    # For now, allow '' and don't allow [] as per user cases.
                    if match.get(kv_pair, something) not in ([],):
                        found_values.append(match.get(kv_pair, something))
                        resource_passed = True

            elif isinstance(values, list):

                for value in values:

                    if isinstance(value, dict):
                        # First search in the keys
                        found_key = seek_key_in_dict(value, something)

                        # The following is an edge case that covers things like aws asg tags (https://www.terraform.io/docs/providers/aws/r/autoscaling_group.html)
                        # Then search in the values with 'key'
                        if not found_key:
                            found_key = seek_regex_key_in_dict_values(value, 'key', something)

                            if found_key:
                                found_key = found_key[0]
                                # not going to use match.get here because the following line is an edge case
                                found_values.extend(value.get('value'))
                                resource_passed = True
                                continue
                    elif isinstance(value, list):
                        _, temp_found_values = it_must_contain_something(_step_obj, something, value, child=True)
                        prop_list.extend(temp_found_values)
                        resource_passed = True

                    elif isinstance(value, (str, bool, int, float)):
                        if match.equals(value, something):
                            found_values.append(value)
                            resource_passed = True

                    if found_key is not Null and len(found_key):

                        for found_key_instance in found_key:
                            if isinstance(found_key_instance, dict):
                                if match.get(found_key_instance, something, Null) not in (Null, [], '', {}):
                                    found_values.append(match.get(found_key_instance, something))
                                    resource_passed = True

            for i, found_val in enumerate(found_values):
                if isinstance(found_val, dict) and 'constant_value' in found_val:
                    found_values[i] = found_val['constant_value']

            for found_val in found_values:
                prop_list.append({'address': resource['address'],
                                'values': found_val,
                                'type': _step_obj.context.name})

            # do not check prop list here because every resource should contain it.
            if not resource_passed and not child: # if nothing was found in this resource, don't error if you're a child
                Error(_step_obj, '{} ({}) does not have {} property.'.format(resource['address'],
                                                                             resource.get('type', ''),
                                                                             something))

        if prop_list:
            _step_obj.context.stash = prop_list
            _step_obj.context.property_name = something
            return something, prop_list

    elif _step_obj.context.type == 'provider':
        prop_list = []
        for provider_data in _step_obj.context.stash:
            values = seek_key_in_dict(provider_data, something)

            if values:
                prop_list.extend(values)
                _step_obj.context.property_name = something
                _step_obj.context.address = '{}.{}'.format(provider_data.get('name', _step_obj.context.addresses),
                                                           provider_data.get('alias', "\b"))

            else:
                Error(_step_obj, '{} {} does not have {} property.'.format(_step_obj.context.addresses,
                                                                           _step_obj.context.type,
                                                                           something))

        if prop_list:
            _step_obj.context.stash = prop_list
            return True

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

            found_values = []
            found_key = Null
            resource_passed = False
            # set this to True if you get anything from the resource, don't set it to False if you get empty values as there could be other values as well
            if isinstance(values, dict):

                found_key = match.get(values, something, Null)
                if found_key is not Null:
                    found_key = [{something: found_key}]
                else:
                    found_key = seek_key_in_dict(values, something)

                for kv_pair in found_key:
                    # kv_pair must be in {something: found_key} format.
                    if not isinstance(kv_pair, dict):
                        continue # could raise an exception
                    # ignore the values that correspond to Null 
                    # Following line could be problematic, how to determine if something is set to be empty or not set? Behavior is provider dependent. 
                    # For now, allow '' and don't allow [] as per user cases.
                    if match.get(kv_pair, something) not in ([],):
                        found_values.append(match.get(kv_pair, something))
                        resource_passed = True

            elif isinstance(values, list):

                for value in values:

                    if isinstance(value, dict):
                        # First search in the keys
                        found_key = seek_key_in_dict(value, something)

                        # Then search in the values with 'key'
                        if not found_key:
                            found_key = seek_regex_key_in_dict_values(value, 'key', something)

                            if found_key:
                                found_key = found_key[0]
                                found_values.extend(value.get('value'))
                                resource_passed = True
                                continue
                    elif isinstance(value, list):
                        _, temp_found_values = it_must_contain_something(_step_obj, something, value, child=True)
                        prop_list.extend(temp_found_values)
                        resource_passed = True

                    elif isinstance(value, (str, bool, int, float)):
                        if match.equals(value, something):
                            found_values.append(value)
                            resource_passed = True

                    if found_key is not Null and len(found_key):

                        for found_key_instance in found_key:
                            if isinstance(found_key_instance, dict):
                                if match.get(found_key_instance, something, Null) not in (Null, [], '', {}):
                                    found_values.append(match.get(found_key_instance, something))
                                    resource_passed = True

            for i, found_val in enumerate(found_values):
                if isinstance(found_val, dict) and 'constant_value' in found_val:
                    found_values[i] = found_val['constant_value']

            if resource_passed:
                Error(_step_obj, '{} property exists in {} ({}).'.format(something, resource['address'], resource.get('type', '')))

    elif _step_obj.context.type == 'provider':
        for provider_data in _step_obj.context.stash:
            values = seek_key_in_dict(provider_data, something)

            if values:
                Error(_step_obj, '{} {} does not have {} property.'.format(_step_obj.context.addresses,
                                                                           _step_obj.context.type,
                                                                           something))
