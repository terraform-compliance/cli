# -*- coding: utf-8 -*-


def i_flatten_everything_found(_step_obj):
    flattened_list = []
    addresses_flattened = []
    for each in _step_obj.context.stash:
        flattened_list.append(each.get('values', each))
        addresses_flattened.append(each.get('address', each))

    if flattened_list:
        _step_obj.context.stash = {
            'address': ', '.join(addresses_flattened),
            'values': flattened_list
        }

    return flattened_list
