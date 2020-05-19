# -*- coding: utf-8 -*-

from terraform_compliance.common.helper import (
    EmptyStash,
    get_resource_name_from_stash
)
from terraform_compliance.common.error_handling import Error
import re


def its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, _stash=EmptyStash, case_insensitive=True):
    def fail(condition, name=None):
        text = 'matches' if condition == 'must not' else 'does not match'
        name = name if (name is not None or name is not False) else _step_obj.context.name
        pattern = 'Null/None' if regex == '\x00' else regex
        Error(_step_obj, '{} property in {} {} {} with {} {} regex. '
                         'It is set to {}.'.format(_step_obj.context.property_name,
                                                   name,
                                                   _step_obj.context.type,
                                                   text,
                                                   pattern,
                                                   regex_flag_error_text,
                                                   values))

    regex = r'{}'.format(search_regex)
    values = _step_obj.context.stash if _stash is EmptyStash else _stash
    regex_flags = re.IGNORECASE if case_insensitive else 0
    regex_flag_error_text = 'case insensitive' if case_insensitive else 'case sensitive'

    if isinstance(values, (str, int, bool)) or values is None:
        matches = re.match(regex, str(values), flags=regex_flags)

        if (condition == 'must' and matches is None) or (condition == "must not" and matches is not None):
            _stash = get_resource_name_from_stash(_step_obj.context.stash, _stash, _step_obj.context.address)
            fail(condition, name=_stash.get('address'))

    elif isinstance(values, list):
        for value in values:
            its_value_condition_match_the_search_regex_regex(_step_obj,
                                                             condition,
                                                             search_regex,
                                                             value,
                                                             case_insensitive=case_insensitive)

    elif isinstance(values, dict):
        if not hasattr(_step_obj.context, 'address'):
            _step_obj.context.address = None

        _step_obj.context.address = values.get('address', _step_obj.context.address)

        if 'values' in values:
            if values['values'] is None and regex == '\x00' and condition == 'must not':
                values = values['values']
                fail(condition, name=_stash.get('address'))
            else:
                its_value_condition_match_the_search_regex_regex(_step_obj,
                                                                 condition,
                                                                 search_regex,
                                                                 values.get('values'),
                                                                 case_insensitive=case_insensitive)

        else:
            for key, value in values.items():
                its_value_condition_match_the_search_regex_regex(_step_obj,
                                                                 condition,
                                                                 search_regex,
                                                                 value,
                                                                 case_insensitive=case_insensitive)
