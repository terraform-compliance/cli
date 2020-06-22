# -*- coding: utf-8 -*-

from terraform_compliance.common.helper import (
    Null,
)
from terraform_compliance.common.error_handling import Error
from terraform_compliance.common.exceptions import TerraformComplianceNotImplemented


def its_key_condition_be_value(_step_obj, key, condition, value, stash=Null, depth=0):
    match = _step_obj.context.match
    seek_regex_key_in_dict_values = match.seek_regex_key_in_dict_values

    if condition not in ('must', 'must not'):
        raise TerraformComplianceNotImplemented('This step only accepts "must" and "must not" as a condition.')
    condition = condition == 'must'

    if stash is Null:
        stash = _step_obj.context.stash

    if not stash or stash is Null:
        Error(_step_obj, 'No entities found for this step to process. Check your filtering steps in this scenario.')
        return False

    obj_address = _step_obj.context.name
    if hasattr(_step_obj.context, 'address'):
        obj_address = _step_obj.context.address
    elif hasattr(_step_obj.context, 'addresses'):
        obj_address = ', '.join(_step_obj.context.addresses)

    found_values = []
    for entity in stash:
        if isinstance(entity, dict):
            found_value = seek_regex_key_in_dict_values(entity, key, value)
            if not found_value and condition:
                Error(_step_obj, 'Can not find {} in {} property of {}.'.format(value, key, match.get(entity, 'address', obj_address)))                
                Error(_step_obj, 'Can not find {} in {} property of {}.'.format(value, key, obj_address)) # legacy error message
            elif found_value and not condition:
                Error(_step_obj, 'Found {}({}) in {} property of {}.'.format(value, ', '.join(found_values), key, obj_address))

            found_values.extend(found_value)

        elif isinstance(entity, list):
            dict_entity = {f'not_{str(key)}': entity}
            found_value = seek_regex_key_in_dict_values(dict_entity, key, value)
            if not found_value and condition:
                Error(_step_obj, 'Can not find {} in {} property of {}.'.format(value, key, obj_address))
            elif found_value and not condition:
                Error(_step_obj, 'Found {}({}) in {} property of {}.'.format(value, ', '.join(found_values), key, obj_address))

            found_values.extend(found_value)

        elif isinstance(entity, (str, int, bool)):
            # raise error because you don't have a {key: value}
            if (match.equals(entity, key) or match.equals(entity, value)) and condition:
                Error(_step_obj, 'Value {} found in {} property of {}, but is not in {{key: value}} format.'.format(value, key, obj_address))
            if condition:
                Error(_step_obj, 'Can not find {} in {} property of {}.'.format(value, key, obj_address))


    _step_obj.context.stash = found_values

    return True
