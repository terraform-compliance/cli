from terraform_compliance.common.defaults import Defaults
from terraform_compliance.common.helper import Match
from terraform_compliance.common.error_handling import Error
import re


def look_for_bdd_tags(_step_obj):
    _step_obj.context.no_failure = False
    _step_obj.context.failure_class = None
    _step_obj.context.no_skip = False
    _step_obj.context.skip_class = None # to pick a tagname that user used
    _step_obj.context.lines_to_noskip = []
    _step_obj.context.bad_tags = False
    _step_obj.context.resources_to_exclude = r''

    defaults = Defaults()

    if hasattr(_step_obj, 'all_tags') and len(_step_obj.all_tags) > 0:
        _step_obj.context.case_insensitivity = True

        for tag in _step_obj.all_tags:
            if tag.name.lower() in defaults.no_failure_tags:
                _step_obj.context.no_failure = True
                _step_obj.context.failure_class = tag.name
            elif tag.name.lower() in defaults.case_sensitive_tags:
                _step_obj.context.case_insensitivity = False
            elif tag.name.lower() in defaults.no_skip_tags:
                _step_obj.context.no_skip = True
                _step_obj.context.skip_class = tag.name
                _step_obj.context.lines_to_noskip = [-1]
            # noskip
            elif re.search(r'({})_at_lines?_.*'.format('|'.join(defaults.no_skip_tags)), tag.name.lower()):
                # check for '@noskip at line x'
                regex = r'({})_at_lines?((_\d*)*)'.format('|'.join(defaults.no_skip_tags))
                
                m = re.search(regex, tag.name.lower())
                if m is not None:
                    _step_obj.context.no_skip = True
                    _step_obj.context.skip_class = tag.name

                    line_numbers_string = m.group(2)

                    try:
                        line_numbers = map(int, line_numbers_string.strip('_').split('_'))
                        if _step_obj.context.lines_to_noskip != [-1]: # no need to worry about this tag if we already have a general noskip
                            _step_obj.context.lines_to_noskip.extend(line_numbers)
                    
                    except Exception as e:
                        Error(_step_obj, f'A tag was determined to be a noskip, but line numbers could not be grouped by the regex {regex}\n{e}')
            # exclude resources
            elif re.search(r'({})_.+\..+'.format('|'.join(defaults.exclude_resources_tags)), tag.name.lower()):
                regex = r'({})_(.+)'.format('|'.join(defaults.exclude_resources_tags))
                
                m = re.search(regex, tag.name.lower())
                if m is not None:
                    resource_address = m.group(2)

                    if _step_obj.context.resources_to_exclude:
                        _step_obj.context.resources_to_exclude += r'|'
                    
                    _step_obj.context.resources_to_exclude += r'({})'.format(resource_address)


    if _step_obj.context.no_failure and _step_obj.context.no_skip:
        _step_obj.context.no_failure = False
        _step_obj.context.bad_tags = True
        Error(_step_obj, f'@{_step_obj.context.failure_class} and @{_step_obj.context.skip_class} tags can not be used at the same time.')

    ## set the match here
    case_sensitive = True if hasattr(_step_obj.context, 'case_insensitivity') and not _step_obj.context.case_insensitivity else False
    _step_obj.context.match = Match(case_sensitive=case_sensitive)

    return _step_obj
