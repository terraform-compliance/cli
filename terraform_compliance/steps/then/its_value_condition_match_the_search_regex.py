# -*- coding: utf-8 -*-

from terraform_compliance.common.helper import (
    EmptyStash,
    get_resource_name_from_stash
)
from terraform_compliance.common.error_handling import Error
import re


def its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, _stash=EmptyStash):
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

    match = _step_obj.context.match
    regex = r'{}'.format(search_regex)
    values = _step_obj.context.stash if _stash is EmptyStash else _stash
    regex_flag_error_text = 'case insensitive' if not match.case_sensitive else 'case sensitive'

    if isinstance(values, (str, int, bool, float)) or values is None:
        matches = match.regex_match(regex, str(values))

        if (condition == 'must' and matches is None) or (condition == "must not" and matches is not None):
            _stash = get_resource_name_from_stash(_step_obj.context.stash, _stash, _step_obj.context.address)
            fail(condition, name=_stash.get('address'))

    elif isinstance(values, list):
        for value in values:
            its_value_condition_match_the_search_regex_regex(_step_obj,
                                                             condition,
                                                             search_regex,
                                                             value)

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
                                                                 values.get('values'))

        else:
            for key, value in values.items():
                its_value_condition_match_the_search_regex_regex(_step_obj,
                                                                 condition,
                                                                 search_regex,
                                                                 value)


def any_of_its_values_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, _stash=EmptyStash):
    def fail(condition, name=None):
        text = 'matches' if condition == 'must not' else 'does not match'
        name = name if (
            name is not None or name is not False) else _step_obj.context.name
        pattern = 'Null/None' if regex == '\x00' else regex
        Error(_step_obj, '{} property in {} {} {} with {} {} regex. '
                         'It is set to {}.'.format(_step_obj.context.property_name,
                                                   name,
                                                   _step_obj.context.type,
                                                   text,
                                                   pattern,
                                                   regex_flag_error_text,
                                                   values))

    found = False
    def search(values):
        nonlocal found
        if found:
            return True

        if isinstance(values, (str, int, bool, float)) or values is None:
            matches = match.regex_match(regex, str(values))

            if (condition == 'must' and matches is not None) or (condition == "must not" and matches is None):
                found = True
                return found

        elif isinstance(values, list):
            return any(map(search, values))

        elif isinstance(values, dict):
            if not hasattr(_step_obj.context, 'address'):
                _step_obj.context.address = None

            _step_obj.context.address = values.get('address', _step_obj.context.address)

            if 'values' in values:
                return search(values['values'])
            else:
                return any(map(search, values.values()))

        return False

    match = _step_obj.context.match
    regex = r'{}'.format(search_regex)
    values = _step_obj.context.stash if _stash is EmptyStash else _stash
    regex_flag_error_text = 'case insensitive' if not match.case_sensitive else 'case sensitive'

    if not search(values):
        _stash = get_resource_name_from_stash(_step_obj.context.stash, _stash, _step_obj.context.address)
        fail(condition, name=_stash.get('address'))


def its_singular_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, _stash=EmptyStash):
    resources = _step_obj.context.stash if _stash is EmptyStash else _stash

    if isinstance(resources, dict): 
        if 'values' in resources: # in case the object is in 'address', 'values', 'type' format
            resources = resources['values']
        else:
            Error(_step_obj, '{} is multivalued! Please use any/all versions of this step instead.'.format(_step_obj.context.property_name,))
            return

    elif isinstance(resources, list):
        for resource in resources:
            if isinstance(resource, dict):
                resource = resource.get('values', resource)

            if isinstance(resource, (dict, list)) and len(resource) > 1:
                Error(_step_obj, '{} is multivalued! Please use any/all versions of this step instead.'.format(_step_obj.context.property_name,))
                return

    its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, _stash)
