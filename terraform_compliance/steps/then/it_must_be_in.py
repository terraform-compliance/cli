from terraform_compliance.common.error_handling import Error

def it_must_be_in(_step_obj, haystack, cover=False):
    match = _step_obj.context.match

    values = [resource['values'] for resource in _step_obj.context.stash]
    parsed_haystack = _step_obj.context.in_step_variables['haystack']

    if not cover and not match.issubset(values, parsed_haystack):
        Error(_step_obj, '{} does not cover selected resources.'.format(haystack))                                                                        

    if cover and not match.issubset(parsed_haystack, values):
        Error(_step_obj, 'Selected resources does not cover {}.'.format(haystack))                                                                        

'''
inherited values?
What if provider?

a covers b
subset(b, a)

a in b
subset(a, b)


'''

