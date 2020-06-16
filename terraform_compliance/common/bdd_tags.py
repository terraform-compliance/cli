from terraform_compliance.common.defaults import Defaults
from terraform_compliance.common.error_handling import Error


def look_for_bdd_tags(_step_obj):
    _step_obj.context.no_failure = False
    _step_obj.context.failure_class = None
    _step_obj.context.skip_class = None

    if hasattr(_step_obj, 'all_tags') and len(_step_obj.all_tags) > 0:
        _step_obj.context.case_insensitivity = True

        for tag in _step_obj.all_tags:
            if tag.name.lower() in Defaults().no_failure_tags:
                _step_obj.context.no_failure = True
                _step_obj.context.failure_class = tag.name
            elif tag.name.lower() in Defaults().case_sensitive_tags:
                _step_obj.context.case_insensitivity = False
            elif tag.name.lower() in Defaults().no_skip_tags:
                _step_obj.context.no_skip = True
                _step_obj.context.skip_class = tag.name

    if hasattr(_step_obj.context, 'no_failure') and hasattr(_step_obj.context, 'no_skip') and _step_obj.context.no_failure:
        _step_obj.context.no_failure = False
        Error(_step_obj, f'@{_step_obj.context.failure_class} and @{_step_obj.context.skip_class} tags can not be used at the same time.')

    return _step_obj
