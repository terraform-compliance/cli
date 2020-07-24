from terraform_compliance.common.exceptions import TerraformComplianceNotImplemented
from terraform_compliance.extensions.ext_radish_bdd import skip_step


def when_its_value_condition_match_the_search_regex_regex(_step_obj, condition, search_regex, any_values=False):
    if condition in ['matches', 'does match']:
        condition = 'must'
    elif condition in ['doesnt match', 'does not match']: # doesn't becomes doesnt during evaluation
        condition = 'must not'
    else:
        raise TerraformComplianceNotImplemented('Incorrect step condition.')

    match = _step_obj.context.match
    regex = r'{}'.format(search_regex)
    # values = _step_obj.context.stash if _stash is EmptyStash else _stash
    regex_flag_error_text = 'case insensitive' if not match.case_sensitive else 'case sensitive'

    prop_list = []
    offending_values = []
    offending_addresses = []

    for resource in _step_obj.context.stash:
        values = resource.get('values', {})

        if isinstance(values, (list, dict)):
            if not any_values:
                bad_resource = False
                for value in values:
                    if not (isinstance(value, (str, int, bool, float)) or value is None):
                        continue

                    matches = match.regex_match(regex, str(value))
                    if (condition == 'must' and matches is None) or (condition == 'must not' and matches is not None):
                        bad_resource = True
                        offending_addresses.append(resource['address'])
                        offending_values.append(values)
                        break
                
                if not bad_resource:
                    prop_list.append(resource)
            else:
                good_resource = False
                for value in values:
                    if not (isinstance(value, (str, int, bool, float)) or value is None):
                        continue

                    matches = match.regex_match(regex, str(value))
                    if (condition == 'must' and matches is not None) or (condition == 'must not' and matches is None):
                        goood_resource = True
                        break
                
                if good_resource:
                    prop_list.append(resource)
                else:
                        offending_addresses.append(resource['address'])
                        offending_values.append(values)

        if isinstance(values, (bool, int, float, str)) or values is None:
            matches = match.regex_match(regex, str(values))

            if (condition == 'must' and matches is not None) or (condition == 'must not' and matches is None):
                prop_list.append(resource)
            else:
                offending_addresses.append(resource['address'])
                offending_values.append(values)

    

    if not prop_list:
        # say matched with all or did not match with any
        # say resource vs resources
        resource_types = list(set(offending_addresses))
        resource_text = f'{resource_types[0]} {_step_obj.context.type}' if len(resource_types) == 1 else '{} {}s'.format(', '.join(resource_types), _step_obj.context.type) # 

        error_texts = ['All values', 'match'] if condition == 'must not' else ['No value', 'matches']
        pattern = 'Null/None' if regex == '\x00' else regex
        
        error_message = f'{error_texts[0]} in {_step_obj.context.property_name} property of {resource_text} {error_texts[1]} with {pattern} {regex_flag_error_text} regex. '
        
        pairs = [f'\t\t{offending_addresses[i]}: {offending_values[i]}' for i in range(len(offending_addresses))]
        pairs = '\n'.join(pairs)
        details = f'They are set to:\n{pairs}'


        skip_step(_step_obj, resource=_step_obj.context.name, message=error_message+details)

    _step_obj.context.stash = prop_list


