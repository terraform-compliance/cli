# -*- coding: utf-8 -*-

from terraform_compliance.steps import property_match_list
from terraform_compliance.common.helper import (
    seek_key_in_dict,
    Null
)
from terraform_compliance.common.error_handling import Error


def property_is_enabled(_step_obj, something):
    for resource in _step_obj.context.stash:
        if isinstance(resource, dict):
            if something in property_match_list:
                something = property_match_list[something].get(resource['type'], something)

            property_value = seek_key_in_dict(resource.get('values', {}), something)

            if len(property_value):
                property_value = property_value[0]

                if isinstance(property_value, dict):
                    property_value = property_value.get(something, Null)

            if not property_value:
                Error(_step_obj, 'Resource {} does not have {} property enabled '
                                 '({}={}).'.format(resource.get('address', "resource"),
                                                   something,
                                                   something,
                                                   property_value))
    return True
