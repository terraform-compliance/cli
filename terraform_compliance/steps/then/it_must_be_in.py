from terraform_compliance.common.error_handling import Error
from terraform_compliance.common.helper import Null

def it_must_be_in(_step_obj, haystack, cover=False):
    match = _step_obj.context.match

    values = [resource['values'] for resource in _step_obj.context.stash]
    for value in values:
        if not isinstance(value, (bool, int, float, str)):
            Error(_step_obj, 'Values are not of the correct type. (bool, str, int, float)')

    if 'haystack' not in _step_obj.context.in_step_variables:
        Error(_step_obj, 'Could not resolve haystack: {}'.format(haystack))       
    parsed_haystack = _step_obj.context.in_step_variables['haystack']

    if not cover and not match.issubset(values, parsed_haystack):
        Error(_step_obj, '{} does not cover selected resources.'.format(haystack))                                                                        

    if cover and not match.issubset(parsed_haystack, values):
        Error(_step_obj, 'Selected resources does not cover {}.'.format(haystack))                                                                        
