# -*- coding: utf-8 -*-

from terraform_compliance.common.defaults import Defaults
from terraform_compliance.common.helper import (
    get_resource_address_list_from_stash,
    Null
)
from terraform_compliance.extensions.ext_radish_bdd import skip_step


def its_key_is_value(_step_obj, key, value, dict_value=None, address=Null):
    def to_lower_key(d):
        return {str(k).lower(): v for k, v in d.items()}

    orig_key = key
    if key == 'reference':
        if address is not Null:
            key = Defaults.r_mount_addr_ptr
        elif address is Null:
            key = Defaults.r_mount_addr_ptr_list
    else:
        key = str(key).lower()

    found_list = []
    for obj in _step_obj.context.stash:
        obj = to_lower_key(obj)
        object_key = obj.get('values', {})
        if isinstance(object_key, list):
            for el in object_key:
                if isinstance(el, dict):
                    el = to_lower_key(el)
                    filtered_key = el.get(key)
                    if isinstance(filtered_key, (str, int, bool)) and str(filtered_key).lower() == str(value).lower():
                        found_list.append(el)
        else:
            object_key = to_lower_key(object_key)
            object_key = object_key.get(key, Null)

        if object_key is Null:
            object_key = obj.get(key, Null)
            if address is not Null and isinstance(object_key, dict) and address in object_key:
                object_key = object_key.get(address, Null)

        if isinstance(object_key, str):
            if "[" in object_key:
                object_key = object_key.split('[')[0]

            if object_key.lower() == value.lower():
                found_list.append(obj)

        elif isinstance(object_key, (int, bool)) and str(object_key).lower() == str(value).lower():
            found_list.append(obj)

        elif isinstance(object_key, list):
            object_key = [str(v).lower() for v in object_key]
            if str(value).lower() in object_key:
                found_list.append(obj)

        elif isinstance(object_key, dict):
            object_key = to_lower_key(object_key)
            candidate_value = object_key.get(str(value).lower())
            if candidate_value is not None and (
                    dict_value is None or (
                    str(candidate_value).lower() == str(dict_value).lower())
            ):
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
    orig_key = key
    if key == 'reference':
        if address is not Null:
            key = Defaults.r_mount_addr_ptr
        elif address is Null:
            key = Defaults.r_mount_addr_ptr_list

    key = str(key).lower()
    found_list = []
    for obj in _step_obj.context.stash:
        object_key = obj.get(key, Null)

        if object_key is Null:
            object_key = obj.get('values', {})
            if isinstance(object_key, list):
                object_keys = []
                for object_key_element in object_key:
                    if str(object_key_element.get(key, Null)).lower() != str(value).lower():
                        object_keys.append(object_key_element.get(key, Null))

                object_key = [keys for keys in object_keys if keys is not Null]
            else:
                object_key = object_key.get(key, Null)

        if address is not Null and isinstance(object_key, dict) and address in object_key:
            object_key = object_key.get(address, Null)

        if isinstance(object_key, str):
            if "[" in object_key:
                object_key = object_key.split('[')[0]

            if object_key != value:
                found_list.append(obj)

        elif isinstance(object_key, (int, bool)) and str(object_key).lower() != str(value).lower():
            found_list.append(obj)

        elif isinstance(object_key, list) and value not in object_key:
            found_list.append(obj)

        elif isinstance(object_key, dict):
            if value not in object_key.keys() or (dict_value is not None and (str(object_key[value]).lower() != str(dict_value).lower())):
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
