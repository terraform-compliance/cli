# -*- coding: utf-8 -*-

from terraform_compliance.common.helper import (
    EmptyStash,
    get_resource_name_from_stash
)
from terraform_compliance.common.error_handling import Error
from terraform_compliance.common.exceptions import TerraformComplianceNotImplemented
from terraform_compliance.common.exceptions import TerraformComplianceInternalFailure


def its_value_condition_contain(_step_obj, condition, value, _stash=EmptyStash):
    match = _step_obj.context.match
    seek_value_in_dict = match.seek_value_in_dict

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
