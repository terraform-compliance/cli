# -*- coding: utf-8 -*-

from terraform_compliance.steps import property_match_list
from terraform_compliance.common.helper import (
    Null
)
from terraform_compliance.common.error_handling import Error


def property_is_enabled(_step_obj, something):
    match = _step_obj.context.match
    seek_key_in_dict = match.seek_key_in_dict

    for resource in _step_obj.context.stash:
        if isinstance(resource, dict):
            if match.contains(property_match_list, something):
                something = match.get(match.get(property_match_list, something), resource['type'], something)

            property_value = seek_key_in_dict(match.get(resource, 'values', {}), something)

            if len(property_value):
                property_value = property_value[0]

                if isinstance(property_value, dict):
                    property_value = match.get(property_value, something, Null)

            if not property_value:
                Error(_step_obj, 'Resource {} does not have {} property enabled '
                                 '({}={}).'.format(resource.get('address', "resource"),
                                                   something,
                                                   something,
                                                   property_value))
    return True
