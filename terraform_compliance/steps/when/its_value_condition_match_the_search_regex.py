from terraform_compliance.common.exceptions import TerraformComplianceNotImplemented
from terraform_compliance.extensions.ext_radish_bdd import skip_step


def when_its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, any_values=False):
    if condition in ['match', 'matches', 'does match']:
        condition = 'must'
    elif condition in ['doesnt match', 'does not match', 'dont match', 'do not match']: # doesn't becomes doesnt during evaluation
        condition = 'must not'
    else:
        raise TerraformComplianceNotImplemented('Incorrect step condition.')

    match = _step_obj.context.match
    regex = r'{}'.format(search_regex)
    regex_flag_error_text = 'case insensitive' if not match.case_sensitive else 'case sensitive'

    prop_list = []
    offending_values = []
    offending_addresses = []
    bad_values_exist = False

    for resource in _step_obj.context.stash:
        values = resource.get('values', {})

        if isinstance(values, (list, dict)):
            # if all values are bad (not compatible with regex), skip this resource.
            if not any(map(lambda x: isinstance(x, (str, int, bool, float)) or x is None, values)):
                bad_values_exist = True
                continue

            resource_condition_matches = [False for value in values]
            for i, value in enumerate(values):
                if not (isinstance(value, (str, int, bool, float)) or value is None):
                    if not any_values:
                        resource_condition_matches[i] = True  # for it to not affect the result
                    continue

                matches = match.regex_match(regex, str(value))
                if (condition == 'must' and matches is not None) or (condition == 'must not' and matches is None):
                    resource_condition_matches[i] = True
            
            if (any_values and any(resource_condition_matches)) or (not any_values and all(resource_condition_matches)):
                prop_list.append(resource)
            else:
                for i, value in enumerate(values):
                    if (isinstance(value, (str, int, bool, float)) or value is None) and not resource_condition_matches[i]:
                        offending_addresses.append(resource['address'])
                        offending_values.append(value)

        if isinstance(values, (bool, int, float, str)) or values is None:
            matches = match.regex_match(regex, str(values))

            if (condition == 'must' and matches is not None) or (condition == 'must not' and matches is None):
                prop_list.append(resource)
            else:
                offending_addresses.append(resource['address'])
                offending_values.append(values)

    

    if not prop_list:
        if not offending_addresses and bad_values_exist:
            skip_step(_step_obj, resource=_step_obj.context.name, message='No value in given stash supports regex comparison.')
        else:
            resource_text = f'{offending_addresses[0]} {_step_obj.context.type}' if len(set(offending_addresses)) == 1 else '{} {}s'.format(', '.join(set(offending_addresses)), _step_obj.context.type) #

            error_texts = ['All instances of', 'match'] if condition == 'must not' else ['No instance of', 'matches']
            pattern = 'Null/None' if regex == '\x00' else regex
            
            error_message = f'{error_texts[0]} {_step_obj.context.property_name} property of {resource_text} {error_texts[1]} with {pattern} {regex_flag_error_text} regex. '
            
            pairs = [f'\t\t{offending_addresses[i]}: {offending_values[i]}' for i in range(len(offending_addresses))]
            pairs = '\n'.join(pairs)
            details = f'They are set to:\n{pairs}'

            skip_step(_step_obj, resource=_step_obj.context.name, message=error_message+details)

    _step_obj.context.stash = prop_list

