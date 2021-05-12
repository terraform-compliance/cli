# -*- coding: utf-8 -*-

from radish import world
from terraform_compliance.common.bdd_tags import look_for_bdd_tags
from terraform_compliance.common.helper import (
    get_resource_address_list_from_stash,
    find_root_by_key,
    remove_mounted_resources,
    transform_asg_style_tags,
    convert_resource_type,
)
from terraform_compliance.extensions.ext_radish_bdd import skip_step
import re


def i_have_name_section_configured(_step_obj, name, type_name='resource', _terraform_config=world):
    '''
    Finds given resource or variable by name and returns it. Skips the step (and further steps) if it is not found.

    :param _step_obj: Internal, step object for radish.
    :param name: String of the name of the resource_type or variable.
    :param type_name: String of the type, either resource(s) or variable(s)
    :param _terraform_config: Internal, terraform configuration.
    :return:
    '''
    assert (type_name in ['resource', 'resources',
                          'variable', 'variables',
                          'output', 'outputs',
                          'provider', 'providers',
                          'data', 'datas']), \
        '{} configuration type does not exist or not implemented yet. ' \
        'Use resource(s), provider(s), variable(s), output(s) or data(s) instead.'.format(type_name)

    if type_name.endswith('s'):
        type_name = type_name[:-1]

    # Process the tags
    _step_obj = look_for_bdd_tags(_step_obj)
    match = _step_obj.context.match

    if not hasattr(_step_obj.context, 'cumulative_stash'):
        _step_obj.context.cumulative_stash = []
    if not hasattr(_step_obj.context, 'stash'):
        _step_obj.context.stash = []

    if name in ('a resource', 'any resource', 'resources'):
        _step_obj.context.type = type_name
        _step_obj.context.name = name
        _step_obj.context.stash = [obj for key, obj in _terraform_config.config.terraform.resources_raw.items()]
        _step_obj.context.cumulative_stash.extend(_step_obj.context.stash)
        _step_obj.context.addresses = get_resource_address_list_from_stash(_step_obj.context.stash)
        _step_obj.context.property_name = type_name
        return True

    elif name in ('an output', 'any output', 'outputs'):
        _step_obj.context.type = 'output'
        _step_obj.context.name = name
        _step_obj.context.stash = [obj for key, obj in _terraform_config.config.terraform.configuration['outputs'].items()]
        _step_obj.context.cumulative_stash.extend(_step_obj.context.stash)
        _step_obj.context.addresses = get_resource_address_list_from_stash(_terraform_config.config.terraform.configuration['outputs'])
        _step_obj.context.property_name = 'output'
        return True

    elif name in ('a variable', 'any variable', 'variables'):
        _step_obj.context.type = 'variable'
        _step_obj.context.name = name
        _step_obj.context.stash = [obj for key, obj in _terraform_config.config.terraform.configuration['variables'].items()]
        _step_obj.context.cumulative_stash.extend(_step_obj.context.stash)
        _step_obj.context.addresses = 'variable'
        _step_obj.context.property_name = 'variable'
        return True

    elif name.startswith('resource that supports'):
        filter_property = re.match(r'resource that supports (.*)', name).group(1)

        resource_types_supports_tags = set(find_root_by_key(_terraform_config.config.terraform.resources_raw,
                                                        filter_property,
                                                        return_key='type'))

        # look for after_unknown values in case they were omitted
        for resource_type, after_unknown_properties in _terraform_config.config.terraform.type_to_after_unknown_properties.items():
            if filter_property in after_unknown_properties:
                resource_types_supports_tags.add(resource_type)

        resource_list = []
        for resource_type in resource_types_supports_tags:
            # Issue-168: Mounted resources causes problem on recursive searching for resources that supports tags
            #            We are removing all mounted resources here for future steps, since we don't need them for
            #            tags checking.
            found_resources = remove_mounted_resources(_terraform_config.config.terraform.find_resources_by_type(resource_type, match))
            found_resources = transform_asg_style_tags(found_resources)
            resource_list.extend(found_resources)

        if resource_list:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = resource_list
            _step_obj.context.cumulative_stash.extend(_step_obj.context.stash)
            _step_obj.context.addresses = get_resource_address_list_from_stash(resource_list)
            _step_obj.context.property_name = type_name
            return True

    elif type_name == 'resource':
        name = convert_resource_type(name)
        resource_list = _terraform_config.config.terraform.find_resources_by_type(name, match)

        if resource_list:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = resource_list
            _step_obj.context.cumulative_stash.extend(_step_obj.context.stash)
            _step_obj.context.addresses = get_resource_address_list_from_stash(resource_list)
            _step_obj.context.property_name = type_name
            return True

    elif type_name == 'variable':
        found_variable = match.get(_terraform_config.config.terraform.variables, name, None)

        if found_variable:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = [found_variable]
            _step_obj.context.cumulative_stash.extend(_step_obj.context.stash)
            _step_obj.context.addresses = name
            _step_obj.context.property_name = type_name
            return True

    elif type_name == 'output':
        found_output = match.get(_terraform_config.config.terraform.outputs, name, None)

        if found_output:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = found_output
            _step_obj.context.cumulative_stash.extend(_step_obj.context.stash)
            _step_obj.context.addresses = name
            _step_obj.context.property_name = type_name
            return True

    elif type_name == 'provider':
        found_provider = _terraform_config.config.terraform.get_providers_from_configuration(name, match)

        if found_provider:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = found_provider
            _step_obj.context.cumulative_stash.extend(_step_obj.context.stash)
            _step_obj.context.addresses = name
            _step_obj.context.address = name
            _step_obj.context.property_name = type_name
            return True

    elif type_name == 'data':
        name = convert_resource_type(name)
        data_list = _terraform_config.config.terraform.find_data_by_type(name, match)

        if data_list:
            _step_obj.context.type = type_name
            _step_obj.context.name = name
            _step_obj.context.stash = data_list
            _step_obj.context.cumulative_stash.extend(_step_obj.context.stash)
            _step_obj.context.addresses = name
            _step_obj.context.address = name
            _step_obj.context.property_name = type_name
            return True

    skip_step(_step_obj, name)