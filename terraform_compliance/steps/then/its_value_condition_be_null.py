from terraform_compliance.common.error_handling import Error
from terraform_compliance.common.helper import Null
import re


def its_value_condition_be_null(_step_obj, condition):
    if condition not in ['must', 'must not']:
        Error(_step_obj, 'Condition must be one of "must" or "must not"')
        return

    condition_must = condition == 'must'

    match = _step_obj.context.match
    regex = r'{}'.format(u'(\x00|^$)$')
    is_null = lambda x: x in ([], {}, None, Null) or (isinstance(x, str) and match.regex_match(regex, x))

    for resource in _step_obj.context.stash:
        values = resource.get('values', {})

        values_is_null = is_null(values)
        if (values_is_null and not condition_must) or (not values_is_null and condition_must):
            Error(_step_obj, '{} property in {} is considered to be {}. It is set to "{}".'.format(_step_obj.context.property_name,
                                                                                                   resource.get('address', _step_obj.context.name),
                                                                                                   'Null' if values_is_null else 'not Null',
                                                                                                   values))


        elif isinstance(values, (dict, list)):

            list_of_inner_values = values.values() if isinstance(values, dict) else values
            # all values in values are considered null
            all_null = all(map(is_null, list_of_inner_values))

            if (all_null and not condition_must) or (not all_null and condition_must):
                Error(_step_obj, 'Multivalued {} property in {} is considered to be {}. It is set to "{}".'.format(_step_obj.context.property_name,
                                                                                                                   resource.get('address', _step_obj.context.name),
                                                                                                                   'Null' if all_null else 'not Null',
                                                                                                                   values))

