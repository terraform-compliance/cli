# -*- coding: utf-8 -*-

from terraform_compliance.common.helper import (
    Null
)
from terraform_compliance.extensions.ext_radish_bdd import skip_step
from terraform_compliance.common.error_handling import Error
from terraform_compliance.main import Step
from radish.utils import console_write
from terraform_compliance.common.defaults import Defaults


def it_contains_something_old(_step_obj, something, inherited_values=Null):
    console_write("\t{} {}: {}".format(Defaults().warning_icon,
                                       Defaults().warning_colour('WARNING'),
                                       Defaults().info_colour('"When it contains {}" step functionality will be changed'
                                                              ' on future versions and the functionality will be same '
                                                              'as "When it has {}" step. Please use the '
                                                              'latter.'.format(something, something))))
    match = _step_obj.context.match
    seek_key_in_dict = match.seek_key_in_dict
    seek_regex_key_in_dict_values = match.seek_regex_key_in_dict_values

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
                    found_key = found_key[0] if len(found_key) == 1 and match.contains(found_key[0], something) else found_key

                    if isinstance(found_key, dict):
                        found_value = match.get(found_key, something, found_key)
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
                        found_key, found_value = it_contains_something_old(_step_obj, something, value)

                    if found_key is not Null and len(found_key):
                        found_key = found_key[0] if len(found_key) == 1 else found_key

                        if isinstance(found_key, dict):
                            found_value.append(match.get(found_key, something, found_key))

            if isinstance(found_value, dict) and 'constant_value' in found_value:
                found_value = found_value['constant_value']

            if found_value is not Null and found_value != [] and found_value != '' and found_value != {}:
                prop_list.append({'address': resource['address'],
                                  'values': found_value,
                                  'type': _step_obj.context.name})

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

    if _step_obj.state != Step.State.FAILED:
        skip_step(_step_obj,
                  resource=_step_obj.context.name,
                  message='Skipping the step since {} type does not have {} property.'.format(_step_obj.context.type,
                                                                                              something))


def it_has_something(_step_obj, something, inherited_values=Null):
    match = _step_obj.context.match
    seek_key_in_dict = match.seek_key_in_dict
    seek_regex_key_in_dict_values = match.seek_regex_key_in_dict_values

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
                found_key = match.get(values, something, Null)
                if found_key is not Null:
                    found_key = [{something: found_key}]
                else:
                    found_key = seek_key_in_dict(values, something)

                if len(found_key):
                    found_key = found_key[0] if len(found_key) == 1 and match.contains(found_key[0], something) else found_key

                    if isinstance(found_key, dict):
                        found_value = match.get(found_key, something, found_key)
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
                        found_key, found_value = it_has_something(_step_obj, something, value)
                    elif isinstance(value, (str, bool, int, float)) and match.equals(value, something):
                        found_key = value
                        found_value.append(found_key)

                    if found_key is not Null and len(found_key):
                        found_key = found_key[0] if len(found_key) == 1 else found_key

                        if isinstance(found_key, dict):
                            found_value.append(match.get(found_key, something, found_key))

            if isinstance(found_value, dict) and 'constant_value' in found_value:
                found_value = found_value['constant_value']

            if found_value not in (Null, [], '', {}):
                prop_list.append(resource)

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
                prop_list.extend(values)
                _step_obj.context.property_name = something
                _step_obj.context.address = '{}.{}'.format(provider_data.get('name', _step_obj.context.addresses),
                                                           provider_data.get('alias', "\b"))

        if prop_list:
            _step_obj.context.stash = prop_list
            return True

    if _step_obj.state != Step.State.FAILED:
        skip_step(_step_obj,
                  resource=_step_obj.context.name,
                  message='Skipping the step since {} type does not have {} property.'.format(_step_obj.context.type,
                                                                                              something))


def it_does_not_have_something(_step_obj, something, inherited_values=Null):
    match = _step_obj.context.match
    seek_key_in_dict = match.seek_key_in_dict
    seek_regex_key_in_dict_values = match.seek_regex_key_in_dict_values

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
                found_key = match.get(values, something, Null)
                if found_key is not Null:
                    found_key = [{something: found_key}]
                else:
                    found_key = seek_key_in_dict(values, something)

                if len(found_key):
                    found_key = found_key[0] if len(found_key) == 1 and match.contains(found_key[0], something) else found_key

                    if isinstance(found_key, dict):
                        found_value = match.get(found_key, something, found_key)
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
                        found_key, found_value = it_has_something(_step_obj, something, value)

                    if found_key is not Null and len(found_key):
                        found_key = found_key[0] if len(found_key) == 1 else found_key

                        if isinstance(found_key, dict):
                            found_value.append(match.get(found_key, something, found_key))

            if isinstance(found_value, dict) and 'constant_value' in found_value:
                found_value = found_value['constant_value']

            if found_value is not Null and found_value != [] and found_value != '' and found_value != {}:
                prop_list.append(resource['address'])


        prop_list = [resource for resource in _step_obj.context.stash if resource['address'] not in prop_list]
        _step_obj.context.property_name = something

        if prop_list:
            _step_obj.context.stash = prop_list
            return something, prop_list

        if _step_obj.state != Step.State.FAILED:
            skip_step(_step_obj,
                      resource=_step_obj.context.name,
                      message='All objects ({}) coming from previous step has {} '
                              'property.'.format(_step_obj.context.name, something))

    elif _step_obj.context.type == 'provider':
        stash = []
        for provider_data in _step_obj.context.stash:
            values = seek_key_in_dict(provider_data, something)

            if values:
                return False
            else:
                stash.append(provider_data)

        if stash:
            _step_obj.context.stash = stash
            _step_obj.context.property_name = something
            return True


    return True
