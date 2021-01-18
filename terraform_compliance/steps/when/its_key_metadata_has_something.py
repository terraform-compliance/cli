from terraform_compliance.common.error_handling import Error
from terraform_compliance.extensions.ext_radish_bdd import skip_step


def its_key_metadata_has_something(_step_obj, key, value, has_step=True):
    match = _step_obj.context.match

    if match.equals(key, 'values'):
        Error(_step_obj, 'The key "values" is not metadata, please use the "When its property has something" step instead.')
    
    found_list = []
    for resource in _step_obj.context.stash:
        # document this behavior
        key_metadata = match.get(resource, key, default={})
        if not isinstance(key_metadata, (list, dict, set)):
            key_metadata = [key_metadata]

        if has_step and not match.contains(key_metadata, value):
            continue
        elif not has_step and match.contains(key_metadata, value):
            continue

        found_list.append(resource)

    _step_obj.context.stash = found_list

    if not found_list:
        if has_step:
            skip_step(_step_obj, message='Could not find "{}" in "{}" metadata.'.format(value, key))
        if not has_step:
            skip_step(_step_obj, message='Found "{}" in "{}" metadata for all resources.'.format(value, key))