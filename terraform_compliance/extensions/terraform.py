import json
from terraform_compliance.common.helper import seek_key_in_dict, flatten_list, Match, merge_dicts, remove_constant_values
import sys
from copy import deepcopy
from radish.utils import console_write
from terraform_compliance.common.defaults import Defaults
from terraform_compliance.extensions.cache import Cache
from terraform_compliance.common.helper import recursive_jsonify, strip_iterations, get_most_child_module


class TerraformParser(object):
    def __init__(self, filename, parse_it=True):
        '''
        This class reads the given terraform plan filename ( in json format ) and assigns required variables for
        further steps in terraform-compliance. If the file is not a json or terraform plan file, then it will be
        checked and exited in prior steps.

        :param filename: terraform plan filename in json format.
        :parse_it: Runs self.parse() if given.

        :return: None
        '''
        self.supported_terraform_versions = (
            '0.12.',
            '0.13.',
            '0.14.',
            '0.15.',
            '1.0.',
        )
        self.supported_format_versions = [
            '0.1',
            '0.2'
        ]

        self.raw = self._read_file(filename)
        self.variables = None
        self.resources = {}

        self.data = {}

        self.providers = {}

        self.configuration = dict(resources={}, variables={})
        self.file_type = "plan"
        self.resources_raw = {}
        self.type_to_after_unknown_properties = {}
        self.parse_it = parse_it

        if parse_it:
            self.cache = Cache()
            self.parse()

    def _version_check(self):
        if self.raw['format_version'] not in self.supported_format_versions:
            print('\nFATAL ERROR: Unsupported terraform plan output format version '
                  '({}).\n'.format(self.raw['format_version']))
            sys.exit(1)

        if not self.raw['terraform_version'].startswith(self.supported_terraform_versions):
            print('\nFATAL ERROR: Unsupported terraform version '
                  '({}).\n'.format(self.raw['terraform_version']))
            sys.exit(1)

        return True

    def _identify_data_file(self):
        if 'values' in self.raw:
            self.file_type = 'state'

    def _read_file(self, filename):
        '''
        Reads the json filename as a dictionary. We are not checking if the file is a json file again, since
        it is already checked in main.py

        :param filename: json filename with full path
        :return: parsed dictionary
        '''
        with open(filename, 'r', encoding='utf-8') as plan_file:
            data = json.load(plan_file)

        return data

    def _parse_variables(self):
        '''
        Assignes all variables that is defined within the terraform plan

        :return: none
        '''
        self.variables = self.raw.get('variables', {})

    def _parse_resources(self):
        '''
        Assigns all resources defined in the terraform plan

        :return: none
        '''

        # Read Cache
        if self.parse_it:
            cache = self.cache.get('resources')
            if cache:
                self.resources = cache
                return

        # Resources ( exists in Plan )
        for findings in seek_key_in_dict(self.raw.get('planned_values', {}).get('root_module', {}), 'resources'):
            for resource in findings.get('resources', []):
                if self.is_type(resource, 'data'):
                    self.data[resource['address']] = resource
                else:
                    self.resources[resource['address']] = resource

        # Resources ( exists in State )
        for findings in seek_key_in_dict(self.raw.get('values', {}).get('root_module', {}), 'resources'):
            for resource in findings.get('resources', []):
                if self.is_type(resource, 'data'):
                    self.data[resource['address']] = resource
                else:
                    self.resources[resource['address']] = resource

        # Resources ( exists in Prior State )
        for findings in seek_key_in_dict(self.raw.get('prior_state', {}).get('values', {}).get('root_module', {}).get('resources', {}), 'resource'):
            for resource in findings.get('resources', []):
                if self.is_type(resource, 'data'):
                    self.data[resource['address']] = resource
                else:
                    self.resources[resource['address']] = resource

        # Child Modules Resources ( exists in State )
        for findings in seek_key_in_dict(self.raw.get('values', {}).get('root_module', {}), 'child_modules'):
            for resource in findings.get('resources', []):
                if self.is_type(resource, 'data'):
                    self.data[resource['address']] = resource
                else:
                    self.resources[resource['address']] = resource

        # Resource Changes ( exists in Plan )
        for finding in self.raw.get('resource_changes', {}):
            resource = deepcopy(finding)
            change = resource.get('change', {})
            actions = change.get('actions', [])
            if actions != ['delete']:
                resource['values'] = change.get('after', {}) # dict_merge(change.get('after', {}), change.get('after_unknown', {}))
                self.remember_after_unknown(resource, change.get('after_unknown', {}))
                if 'change' in resource:
                    del resource['change']

                if self.is_type(resource, 'data'):
                    self.data[resource['address']] = resource
                else:
                    self.resources[resource['address']] = resource

        if self.parse_it:
            self.cache.set('resources', self.resources)

    def remember_after_unknown(self, resource, after_unknown):
        '''
        Creates a map of resource type to after_unknown values
        These can be used in given step "resource that supports x"

        Note: This function may be extended to capture 'after' values as well. That would require flattening the multi level
        dictionaries in resource
        '''

        # get type
        resource_type = resource.get('type', '')

        # if resource doesn't have type field, try to extract it from address (ideally, this if never evaluates true)
        if not resource_type and 'address' in resource and resource['address']:
            parsed_address = resource.get('address').split('.')
            if parsed_address != 'module':
                resource_type = parsed_address[0]
            elif len(parsed_address) >= 3:
                resource_type = parsed_address[2]
            else:
                return

        # get after_unknown values

        # need to merge because which values are in after_unknown may change from instance to instance
        # merging rule: if field not in map, add it
        if resource_type not in self.type_to_after_unknown_properties:
            self.type_to_after_unknown_properties[resource_type] = after_unknown
        else:
            for key, value in after_unknown.items():
                if key not in self.type_to_after_unknown_properties[resource_type]:
                    self.type_to_after_unknown_properties[resource_type][key] = value

    def _parse_configurations(self):
        '''
        Assigns all configuration related data defined in the terraform plan. This is mostly used for
        resources referencing each other.

        :return: none
        '''

        # Read Cache
        if self.parse_it:
            cache = self.cache.get('configuration')
            if cache:
                self.configuration = cache
                return

        # Resources
        self.configuration['resources'] = {}

        # root resources
        resources = self.raw.get('configuration', {}).get('root_module', {}).get('resources', [])

        # Append module resources
        resources.extend(self.process_module_calls(self.raw.get('configuration', {}).get('root_module', {}).get("module_calls", {})))

        remove_constant_values(resources)
        for resource in resources:
            if self.is_type(resource, 'data'):
                self.data[resource['address']] = resource

            else:
                self.configuration['resources'][resource['address']] = resource

        # Variables
        self.configuration['variables'] = {}
        for findings in seek_key_in_dict(self.raw.get('configuration', {}).get('root_module', {}), 'variables'):
            self.configuration['variables'] = findings.get('variables')

        # Providers
        self.configuration['providers'] = {}
        for findings in seek_key_in_dict(self.raw.get('configuration', {}), 'provider_config'):
            self.configuration['providers'] = findings.get('provider_config', {})

        # Outputs
        self.configuration['outputs'] = {}
        for findings in seek_key_in_dict(self.raw.get('configuration', {}), 'outputs'):
            for key, value in findings.get('outputs', {}).items():
                tmp_output = dict(address=key, value={})
                if 'expression' in value:
                    if 'references' in value['expression']:
                        tmp_output['value'] = value['expression']['references']
                        tmp_output['type'] = 'object'
                    elif 'constant_value' in value['expression']:
                        tmp_output['value'] = value['expression']['constant_value']

                if 'sensitive' in value:
                    tmp_output['sensitive'] = str(value['sensitive']).lower()
                else:
                    tmp_output['sensitive'] = 'false'

                if 'type' in value:
                    tmp_output['type'] = value['type']
                elif 'type' not in tmp_output:
                    if isinstance(tmp_output['value'], list):
                        tmp_output['type'] = 'list'
                    elif isinstance(tmp_output['value'], dict):
                        tmp_output['type'] = 'map'
                    elif isinstance(tmp_output['value'], str):
                        tmp_output['type'] = 'string'
                    elif isinstance(tmp_output['value'], int):
                        tmp_output['type'] = 'integer'
                    elif isinstance(tmp_output['value'], bool):
                        tmp_output['type'] = 'boolean'

                self.configuration['outputs'][key] = tmp_output

        if self.parse_it:
            self.cache.set('configuration', self.configuration)

    def _mount_resources(self, source, target, ref_type):
        '''
        Mounts values of the source resource to the target resource's values with ref_type key

        :param source: source resource
        :param target: target resource
        :param ref_type: reference type (e.g. ingress )
        :return: none
        '''
        for source_resource in source:

            if 'values' not in self.resources.get(source_resource, {}):
                continue
            for parameter, target_resources in target.items():
                for target_resource in target_resources:
                    if target_resource not in self.resources or 'values' not in self.resources[target_resource]:
                        continue

                    resource = self.resources_raw[source_resource]['values']

                    # This is a very stupid terraform-provider bug. Somehow, sometimes it loses the state
                    # and sets the value to None - which is normally not allowed.. It should have been an empty
                    # dict instead. Hence, we are fixing that here.
                    if resource is None:
                        defaults = Defaults()
                        console_write('{} {}: {}'.format(defaults.warning_icon,
                                                         defaults.warning_colour('WARNING (mounting)'),
                                                         defaults.info_colour('The resource "{}" has no values set. This is a terraform provider '
                                                                              'bug. Its recommended to remove/fix this resource within your state.'.format(source_resource))))
                        self.resources_raw[source_resource]['values'] = {}
                        self.resources[source_resource]['values'] = {}
                        resource = {}

                    resource[Defaults.mounted_ptr] = True

                    if Defaults.r_mount_ptr not in self.resources[target_resource]:
                        self.resources[target_resource][Defaults.r_mount_ptr] = {}

                    if Defaults.r_mount_addr_ptr not in self.resources[target_resource]:
                        self.resources[target_resource][Defaults.r_mount_addr_ptr] = {}

                    if Defaults.r_mount_addr_ptr_list not in self.resources[target_resource]:
                        self.resources[target_resource][Defaults.r_mount_addr_ptr_list] = []

                    # ensure resources[target_resource]['values'] is an
                    # empty dict and not None
                    if not self.resources[target_resource]['values']:
                        self.resources[target_resource]['values'] = dict()

                    if ref_type not in self.resources[target_resource]['values']:
                        self.resources[target_resource]['values'][ref_type] = []

                    self.resources[target_resource]['values'][ref_type].append(resource)
                    self.resources[target_resource][Defaults.r_mount_ptr][parameter] = ref_type
                    self.resources[target_resource][Defaults.r_mount_addr_ptr][parameter] = source
                    target_set = set(self.resources[target_resource][Defaults.r_mount_addr_ptr_list])
                    source_set = set(source)
                    self.resources[target_resource][Defaults.r_mount_addr_ptr_list] = list(target_set | source_set)

                    if parameter not in self.resources[source_resource]['values']:
                        self.resources[source_resource]['values'][parameter] = target_resource

    def _find_resource_from_name(self, resource_name, module_address=None):
        '''
        Finds all the resources that is starting with resource_name

        :param resource_name: The first initials of the resource
        :param module_address: Full module address (without the resource)
        :return: list of the found resources
        '''
        if resource_name in self.resources:
            return [resource_name]

        resource_list = []
        # Try to find the resource with the module address in self.resources
        if module_address is not None:
            full_address = '{}.{}'.format(module_address, resource_name)
            if full_address in self.resources:
                return [full_address]

            for key, value in self.resources.items():
                if not key.startswith(module_address):
                    continue

                # Check if the resource/module has iterations
                if '[' in key:
                    # Possibly module (or resource) is using foreach/count
                    k = strip_iterations(key)
                    if k == strip_iterations(full_address):
                        resource_list.append(key)
                else:
                    # Resource/module does not have any iteration
                    # Additionally, the resource we are looking under this module is coming from another
                    # module output. Thus, we need to dive a bit deeper.
                    if resource_name.startswith('module') and key.startswith('module'):
                        resource_list.append(key)

            if resource_list:
                return resource_list

        resource_type, resource_id = resource_name.split('.')[0:2]

        if resource_type == 'module':
            # TODO: This wont work correctly, if an output is used within a module, coming from another module.
            #       Fix multi-layer module structure for the outputs ?
            module_name, output_id = resource_name.split('.')[1:3]
            module = self.raw['configuration']['root_module'].get('module_calls', {}).get(module_name, {})

            output_value = module.get('module', {}).get('outputs', {}).get(output_id, {})

            resources = output_value.get('expression', {}).get('references', []) if 'expression' in output_value else output_value.get('value', [])

            resources = ['{}.{}.{}'.format(resource_type, module_name, res) for res in resources]

            if not resources:
                for key, _ in self.resources.items():
                    if key.startswith(resource_name):
                        resources.append(key)

            if resources:
                resource_list.extend(resources)
        else:
            for key, value in self.resources.items():
                if value['type'] == resource_type and value['name'] == resource_id:
                    resource_list.append(key)

        return resource_list

    def _mount_references(self):
        '''
        Find the references that is defined in self.configuration
        :return:
        '''
        self.resources_raw = deepcopy(self.resources)
        invalid_references = ('var.', 'each.', 'count.')

        # This section will link resources found in configuration part of the plan output.
        # The reference should be on both ways (A->B, B->A) since terraform sometimes report these references
        # in opposite ways, depending on the provider structure.
        for resource in self.configuration['resources']:
            relative_resource_address = '{}.{}'.format(self.configuration['resources'][resource]['type'], self.configuration['resources'][resource]['name'])
            current_module_address = self.configuration['resources'][resource]['address'].replace('.{}'.format(relative_resource_address), '')

            if 'expressions' in self.configuration['resources'][resource]:
                ref_list = {}

                for key, value in self.configuration['resources'][resource]['expressions'].items():
                    references = seek_key_in_dict(value, 'references') if isinstance(value, (dict, list)) else []

                    valid_references = []
                    for ref in references:
                        if isinstance(ref, dict) and ref.get('references'):
                            valid_references = []
                            for r in ref['references']:
                                if r.startswith('var'):
                                    # Try to track the resource given by a variable
                                    _var = self._fetch_resource_by_a_variable(current_module_address, r)
                                    if _var:
                                        valid_references.extend(_var)

                                if not r.startswith(invalid_references):
                                    valid_references.append(r)

                    for ref in valid_references:
                        # if ref is not in the correct format, handle it
                        if len(ref.split('.')) < 3 and ref.startswith('module'):

                            # Using for_each and modules together may introduce an issue where the plan.out.json won't
                            # include the necessary third part of the reference. It is partially resolved by mounting
                            # the reference to all instances belonging to the module
                            if 'for_each_expression' in self.configuration['resources'][resource]:

                                # extract source resources
                                assumed_source_resources = [k for k in self.resources.keys() if k.startswith(resource)]
                                # extract for_each keys
                                assumed_for_each_keys = [k[len(resource):].split('.')[0] for k in assumed_source_resources]
                                # combine ref with for each keys
                                assumed_refs = ['{}{}'.format(ref, key) for key in assumed_for_each_keys]
                                # get all the resources that start with updated ref
                                ambiguous_references = []
                                for r in self.resources.keys():
                                    for assumed_ref in assumed_refs:
                                        if r.startswith(assumed_ref):
                                            if key in ref_list:
                                                ref_list[key].append(r)
                                            else:
                                                ref_list[key] = [r]

                                            ambiguous_references.append(r)

                                # throw a warning
                                defaults = Defaults()
                                console_write('{} {}: {}'.format(defaults.warning_icon,
                                       defaults.warning_colour('WARNING (mounting)'),
                                       defaults.info_colour('The reference "{}" in resource {} is ambigious.'
                                        ' It will be mounted to the following resources:').format(ref, resource)))
                                for i, r in enumerate(ambiguous_references, 1):
                                    console_write(defaults.info_colour('{}. {}'.format(i, r)))

                            # if the reference can not be resolved, warn the user and continue.
                            else:
                                console_write('{} {}: {}'.format(Defaults().warning_icon,
                                       Defaults().warning_colour('WARNING (mounting)'),
                                       Defaults().info_colour('The reference "{}" in resource {} is ambigious. It will not be mounted.'.format(ref, resource))))
                                continue
                        elif key not in ref_list:
                            ref_list[key] = self._find_resource_from_name(ref, current_module_address)
                        else:
                            ref_list[key].extend(self._find_resource_from_name(ref, current_module_address))

                    # This is where we synchronise constant_value in the configuration section with the resource
                    # for filling up the missing elements that hasn't been defined in the resource due to provider
                    # implementation.
                    target_resource = [t for t in [self.resources.get(resource, {}).get('address')] if t is not None]
                    if not target_resource:
                        target_resource = [k for k in self.resources.keys() if k.startswith(resource)]

                    for t_r in target_resource:
                        if self.resources[t_r].get('values') is None:
                            continue
                        if type(value) is type(self.resources[t_r]['values'].get(key)) and self.resources[t_r]['values'].get(key) != value:
                            if isinstance(value, (list, dict)):
                                merge_dicts(self.resources[t_r]['values'][key], value)

                if ref_list:
                    ref_type = self.configuration['resources'][resource]['expressions'].get('type', {})

                    if 'references' in ref_type:
                        ref_type = resource.split('.')[0]

                    if not ref_type and not self.is_type(resource, 'data'):
                        ref_type = self.extract_resource_type_from_address(resource)

                    for k, v in ref_list.items():
                        v = flatten_list(v)

                    # Mounting A->B
                    source_resources = self._find_resource_from_name(self.configuration['resources'][resource]['address'])

                    # Try again in case we might have for_each/count usage for the module
                    if not source_resources:
                        source_resources = self._find_resource_from_name(relative_resource_address, current_module_address)

                    self._mount_resources(source=source_resources,
                                          target=ref_list,
                                          ref_type=ref_type)

                    # Mounting B->A
                    for parameter, target_resources in ref_list.items():
                        for target_resource in target_resources:
                            if not self.is_type(resource, 'data') and not self.is_type(resource, 'var') and not self.is_type(resource, 'provider'):
                                ref_type = self.extract_resource_type_from_address(target_resource)

                                self._mount_resources(source=[target_resource],
                                                      target={parameter: source_resources},
                                                      ref_type=ref_type)

    def _distribute_providers(self):
        for resource_name, resource_data in self.resources.items():
            resource_provider = resource_name.split('_')[0]

            if resource_provider not in self.providers:
                self.providers[resource_provider] = {}

            self.providers[resource_provider][resource_name] = resource_data

    def parse(self):
        '''
        Main method for initialising the parsing of the terraform plan json file

        :return: nothing
        '''
        self._version_check()
        self._identify_data_file()
        self._parse_resources()

        if self.file_type == 'plan':
            self._parse_variables()
            self._parse_configurations()

        cache_mounted_resources = self.cache.get('mounted_resources') if self.parse_it else None
        cache_raw_resources = self.cache.get('resources_raw') if self.parse_it else None
        cache_type_to_after_unknown_properties = self.cache.get('type_to_after_unknown_properties') if self.parse_it else None

        if cache_mounted_resources and cache_raw_resources:
            # print('Read from cache, instead of re-mounting.')
            self.resources = cache_mounted_resources
            self.resources_raw = cache_raw_resources
            self.type_to_after_unknown_properties = cache_type_to_after_unknown_properties
        else:
            # print('Building cache for mounted resources at {}'.format(Defaults.cache_dir))
            self._mount_references()
            # metadata related calls
            self._add_action_status()
            self._add_module_call_source()

            self.resources = recursive_jsonify(self.resources)
            self.resources_raw = recursive_jsonify(self.resources_raw)
            self.type_to_after_unknown_properties = recursive_jsonify(self.type_to_after_unknown_properties)
            self.variables = recursive_jsonify(self.variables)
            self.data = recursive_jsonify(self.data)
            self.providers = recursive_jsonify(self.providers)

            if self.parse_it:
                self.cache.set('mounted_resources', self.resources)
                self.cache.set('resources_raw', self.resources_raw)
                self.cache.set('type_to_after_unknown_properties', self.type_to_after_unknown_properties)

        self._distribute_providers()

        for _, resource in self.resources.items():
            self._expand_resource_tags(resource)

    def _add_action_status(self):
        '''
        Adds Terraform's action status to each resource
        '''
        if 'resource_changes' not in self.raw:
            return

        for resource_change in self.raw['resource_changes']:
            resource = resource_change['address']
            if resource in self.resources:
                self.resources[resource]['actions'] = resource_change['change']['actions']

    def _add_module_call_source(self):
        '''
        Adds module call's source to module's resources as metadata
        '''
        for resource in self.resources.values():
            # removes the for_each signature from addresses
            # module.a["index_1"].b.c -> module.a.b.c
            fixed_module_name = '.'.join([word.split('[')[0] for word in resource['address'].split('.')])

            if 'source' in self.configuration['resources'].get(fixed_module_name, ''):
                resource['source'] = self.configuration['resources'][fixed_module_name]['source']


    def find_resources_by_type(self, resource_type, match=Match(case_sensitive=False)):
        '''
        Finds all resources matching with the resource_type

        :param resource_type: String of resource type defined in terraform
        :return: list of dict including resources
        '''
        resource_list = []

        for resource_data in self.resources.values():
            if resource_type == 'any' or (match.equals(resource_data['type'], resource_type) and resource_data['mode'] == 'managed'):
                resource_list.append(resource_data)

        return resource_list

    def find_data_by_type(self, resource_type, match=Match(case_sensitive=False)):
        '''
        Finds all data matching with the resource_type

        :param resource_type: String of resource type defined in terraform
        :return: list of dict including resources
        '''
        resource_list = []

        for resource_data in self.data.values():
            if match.equals(resource_data['type'], resource_type):
                resource_list.append(resource_data)

        return resource_list

    def get_providers_from_configuration(self, provider_type, match=Match(case_sensitive=False)):
        '''
        Returns all providers as a list for the given provider type

        :param provider_type: String of a provider type like aws
        :return: list of providers that has this type
        '''
        providers = []
        for provider_alias, values in self.configuration['providers'].items():
            if isinstance(values, dict) and match.equals(values.get('name'), provider_type):
                providers.append(values)

        return providers

    def _expand_resource_tags(self, resource):
        if isinstance((resource.get('values') or {}).get('tags'), list):
            for tag in resource.get('values', {}).get('tags', {}):
                if isinstance(tag, dict) and 'key' in tag and 'value' in tag:
                    tag[tag['key']] = tag['value']
            return True
        return False

    def is_type(self, resource, mode):
        if isinstance(resource, dict):
            if 'mode' in resource:
                return resource['mode'] == mode

            return resource['address'].split('.')[0] == mode

        return False

    def process_module_calls(self, module_resource, parents_modules=None):
        '''
        This method will recursively process modules and extract resources from "module_resource" data
        which is actually a data from self.configuration dict. We were returning the native resource name
        before this method, but now we are returning proper address naming for the resource.

        :param module_resource: The self.configuration part
        :param parents_modules: internal usage for recursive functionality
        :return: None
        '''
        if parents_modules is None:
            parents_modules = []

        resources = []
        for k, v in module_resource.items():
            # Set the naming correct (for cases like module.a.module.b.module.c...)
            current_module_level = deepcopy(parents_modules)
            current_module_level.append('module.{}'.format(k))
            module_name = ".".join(current_module_level)
            # Pull module's source to be later used in metadata
            module_source = v.get('source', '')

            # Register the resource (along with module naming)
            if 'resources' in v.get('module', {}):
                for resource in v['module']['resources']:
                    resource['address'] = '{}.{}'.format(module_name, resource['address'])
                    resource['source'] = module_source
                    resources.append(resource)

            # Dive deeper, its not finished yet.
            if 'module_calls' in v.get('module', {}):
                resources.extend(self.process_module_calls(v['module']['module_calls'], current_module_level))

        return resources

    def extract_resource_type_from_address(self, resource_address_string):
        '''
        Tries to get the resource type from the resource address

        :param resource_address_string: String of the whole resource address
        :return: String of the resource type if found, otherwise will return full address

        Example;

            "aws_s3_bucket.test" will return "aws_s3_bucket"
            "module_a.module_b.module_c.aws_s3_bucket.test" will return "aws_s3_bucket"
            "something_else" will return "something_else"
        '''
        if '.' in resource_address_string:
            octets = resource_address_string.split('.')
            if len(octets) > 1:
                # Return the type as we found it properly
                return octets[-2]
            else:
                # Return the whole address
                return octets[0]

        # Returning the whole address
        return resource_address_string

    def _fetch_resource_by_a_variable(self, module, variable):
        target_module = get_most_child_module(module)
        stripped_variable = variable.replace('var.', '')
        var = self.raw['configuration'].get('root_module', {}).get('module_calls', {}).get(target_module, {}).get('expressions', {}).get(stripped_variable, {}).get('references', {})
        return var