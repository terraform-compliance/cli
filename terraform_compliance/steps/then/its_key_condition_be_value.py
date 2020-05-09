# -*- coding: utf-8 -*-

from terraform_compliance.common.helper import (
    Null,
    seek_regex_key_in_dict_values
)
from terraform_compliance.common.error_handling import Error
from terraform_compliance.common.exceptions import TerraformComplianceNotImplemented


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
