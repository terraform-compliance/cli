# -*- coding: utf-8 -*-

from terraform_compliance.common.defaults import Defaults
from terraform_compliance.common.helper import (
    EmptyStash,
    Null
)
from terraform_compliance.common.exceptions import TerraformComplianceNotImplemented
from terraform_compliance.common.error_handling import Error


def i_action_them(_step_obj, action_type):
    match = _step_obj.context.match
    seek_key_in_dict = match.seek_key_in_dict

    if action_type == "count":
        # WARNING: Only case where we set stash as a dictionary, instead of a list.
        if isinstance(_step_obj.context.stash, list):

            # This means we are directly started counting without drilling down any property
            # Thus, our target for the count is stash itself.
            if match.contains(Defaults().types_list, _step_obj.context.property_name):
                _step_obj.context.stash = dict(values=len(_step_obj.context.stash))

            else:
                if isinstance(_step_obj.context.stash[0], dict):
                    if _step_obj.context.stash[0].get('values'):
                        _step_obj.context.stash = seek_key_in_dict(_step_obj.context.stash, 'values')
                        count = 0
                        for result in _step_obj.context.stash:
                            count += len(result.get('values', {})) if result.get('values') and not isinstance(result.get('values'), (int,bool,str)) else 1

                        _step_obj.context.stash = dict(values=count)

                else:
                    _step_obj.context.stash = dict(values=len(_step_obj.context.stash))
    else:
        raise TerraformComplianceNotImplemented('Invalid action_type in the scenario: {}'.format(action_type))


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
