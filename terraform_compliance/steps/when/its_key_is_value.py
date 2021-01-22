# -*- coding: utf-8 -*-

from terraform_compliance.common.defaults import Defaults
from terraform_compliance.common.helper import (
    get_resource_address_list_from_stash,
    Null
)
from terraform_compliance.extensions.ext_radish_bdd import skip_step


def its_key_is_value(_step_obj, key, value, dict_value=None, address=Null):
    match = _step_obj.context.match
    
    orig_key = key
    if key == 'reference':
        if address is not Null:
            key = Defaults.r_mount_addr_ptr
        elif address is Null:
            key = Defaults.r_mount_addr_ptr_list

    found_list = []
    for obj in _step_obj.context.stash:
        object_key = obj.get('values', {})
        if isinstance(object_key, list):
            for el in object_key:
                if isinstance(el, dict):
                    filtered_key = match.get(el, key)
                    if isinstance(filtered_key, (str, int, bool)) and match.equals(filtered_key, value):
                        found_list.append(el)
        else:
            object_key = match.get(object_key, key, Null)

        if object_key is Null:
            object_key = match.get(obj, key, Null)
            if address is not Null and isinstance(object_key, dict) and match.contains(object_key, address):
                object_key = match.get(object_key, address, Null)

        if isinstance(object_key, str):
            if "[" in object_key:
                object_key = object_key.split('[')[0]

            if match.equals(object_key, value):
                found_list.append(obj)

        elif isinstance(object_key, (int, bool)) and match.equals(object_key, value):
            found_list.append(obj)

        elif isinstance(object_key, list):
            object_key = [str(v) for v in object_key]
            if match.contains(object_key, value):
                found_list.append(obj)

        elif isinstance(object_key, dict):
            candidate_value = match.get(object_key, value)
            if candidate_value is not None and (
                    dict_value is None or (
                    match.equals(candidate_value, dict_value))
            ):
                found_list.append(obj)

        elif object_key is None and match.equals('None', value):
            found_list.append(obj)

    if found_list != []:
        _step_obj.context.stash = found_list
        _step_obj.context.addresses = get_resource_address_list_from_stash(found_list)
    else:
        if object_key is Null:
            skip_step(_step_obj, message='Could not find {} in {}.'.format(key,
                                                                           ', '.join(_step_obj.context.addresses)))
        elif dict_value is None:
            skip_step(_step_obj, message='Can not find {} {} in {}.'.format(value, orig_key,
                                                                            ', '.join(_step_obj.context.addresses)))
        else:
            skip_step(_step_obj, message='Can not find {}={} {} in {}.'.format(value, dict_value, orig_key,
                                                                               ', '.join(_step_obj.context.addresses)))


def its_key_is_not_value(_step_obj, key, value, dict_value=None, address=Null):
    match = _step_obj.context.match
    
    orig_key = key
    if key == 'reference':
        if address is not Null:
            key = Defaults.r_mount_addr_ptr
        elif address is Null:
            key = Defaults.r_mount_addr_ptr_list

    found_list = []
    for obj in _step_obj.context.stash:
        object_key = obj.get('values', {})

        if isinstance(object_key, list):
            object_keys = []
            for object_key_element in object_key:
                if not match.equals(match.get(object_key_element, key, Null), value):
                    object_keys.append(match.get(object_key_element, key, Null))

            object_key = [keys for keys in object_keys if keys is not Null]
        else:
            object_key = match.get(object_key, key, Null)
        
        # temporary logic
        # check metadata if key is not in values
        if object_key is Null:
            object_key = match.get(obj, key, Null)

        if address is not Null and isinstance(object_key, dict) and match.contains(object_key, address):
            object_key = match.get(object_key, address, Null)

        if isinstance(object_key, str):
            if "[" in object_key:
                object_key = object_key.split('[')[0]

            if not match.equals(object_key, value):
                found_list.append(obj)

        elif isinstance(object_key, (int, bool)) and not match.equals(object_key, value):
            found_list.append(obj)

        elif isinstance(object_key, list) and not match.contains(object_key, value):
            found_list.append(obj)

        elif isinstance(object_key, dict):
            if not match.contains(object_key, value) or (dict_value is not None and not match.equals(str(match.get(object_key, value)), dict_value)):
                found_list.append(obj)

        elif object_key is None and not match.equals('None', value):
            found_list.append(obj)

    if found_list != []:
        _step_obj.context.stash = found_list
        _step_obj.context.addresses = get_resource_address_list_from_stash(found_list)
    else:
        if object_key is Null:
            skip_step(_step_obj, message='Could not find {} in {}.'.format(key,
                                                                     ', '.join(_step_obj.context.addresses)))
        elif dict_value is None:
            skip_step(_step_obj, message='Found {} {} in {}.'.format(value, orig_key,
                                                                     ', '.join(_step_obj.context.addresses)))
        else:
            skip_step(_step_obj, message='Found {}={} {} in {}.'.format(value, dict_value, orig_key,
                                                                        ', '.join(_step_obj.context.addresses)))
