import json
from terraform_compliance.common.helper import seek_key_in_dict, flatten_list, dict_merge, Match
import sys
from copy import deepcopy
from terraform_compliance.common.defaults import Defaults
from terraform_compliance.extensions.cache import Cache


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
            '0.13.'
        )
        self.supported_format_versions = ['0.1']

        self.raw = self._read_file(filename)
        self.variables = None
        self.resources = {}

        self.data = {}

        self.providers = {}

        self.configuration = dict(resources={}, variables={})
        self.file_type = "plan"
        self.resources_raw = {}
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
                resource['values'] = dict_merge(change.get('after', {}), change.get('after_unknown', {}))
                if 'change' in resource:
                    del resource['change']

                if self.is_type(resource, 'data'):
                    self.data[resource['address']] = resource
                else:
                    self.resources[resource['address']] = resource

        if self.parse_it:
            self.cache.set('resources', self.resources)

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

        resources = []

        # root resources
        resources = self.raw.get('configuration', {}).get('root_module', {}).get('resources', [])

        # Append module resources
        for module in seek_key_in_dict(self.raw.get('configuration', {}).get('root_module', {}).get("module_calls", {}), "module"):
            resources += module.get('module',{}).get("resources", [])

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
        :param target:  target resource
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
                    resource[Defaults.mounted_ptr] = True

                    if Defaults.r_mount_ptr not in self.resources[target_resource]:
                        self.resources[target_resource][Defaults.r_mount_ptr] = {}

                    if Defaults.r_mount_addr_ptr not in self.resources[target_resource]:
                        self.resources[target_resource][Defaults.r_mount_addr_ptr] = {}

                    if Defaults.r_mount_addr_ptr_list not in self.resources[target_resource]:
                        self.resources[target_resource][Defaults.r_mount_addr_ptr_list] = []

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

    def _find_resource_from_name(self, resource_name):
        '''
        Finds all the resources that is starting with resource_name

        :param resource_name: The first initials of the resource
        :return: list of the found resources
        '''
        if resource_name in self.resources:
            return [resource_name]

        resource_list = []

        resource_type, resource_id = resource_name.split('.')[0:2]

        if resource_type == 'module':
            module_name, output_id = resource_name.split('.')[1:3]
            module = self.raw['configuration']['root_module'].get('module_calls', {}).get(module_name, {})

            output_value = module.get('module', {}).get('outputs', {}).get(output_id, {})

            resources = output_value.get('expression', {}).get('references', []) if 'expression' in output_value else output_value.get('value', [])

            resources = ['{}.{}.{}'.format(resource_type, module_name, res) for res in resources]

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
        invalid_references = ('var.')

        # This section will link resources found in configuration part of the plan output.
        # The reference should be on both ways (A->B, B->A) since terraform sometimes report these references
        # in opposite ways, depending on the provider structure.
        for resource in self.configuration['resources']:
            if 'expressions' in self.configuration['resources'][resource]:
                ref_list = {}
                for key, value in self.configuration['resources'][resource]['expressions'].items():
                    if 'references' in value:
                        for ref in value['references']:
                            if not ref.startswith(invalid_references):
                                if key not in ref_list:
                                    ref_list[key] = self._find_resource_from_name(ref)
                                else:
                                    ref_list[key].extend(self._find_resource_from_name(ref))

                if ref_list:
                    ref_type = self.configuration['resources'][resource]['expressions'].get('type',
                                                                                            {}).get('constant_value',
                                                                                                    {})

                    if not ref_type and not self.is_type(resource, 'data'):
                        resource_type, resource_id = resource.split('.')
                        ref_type = resource_type

                    for k, v in ref_list.items():
                        v = flatten_list(v)

                    # Mounting A->B
                    source_resources = self._find_resource_from_name(self.configuration['resources'][resource]['address'])
                    self._mount_resources(source=source_resources,
                                          target=ref_list,
                                          ref_type=ref_type)
                    
                    # Mounting B->A
                    for parameter, target_resources in ref_list.items():
                        for target_resource in target_resources:
                            if not self.is_type(resource, 'data') and not self.is_type(resource, 'var') and not self.is_type(resource, 'provider'):
                                ref_type = target_resource.split('.', maxsplit=1)[0]

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

        if cache_mounted_resources and cache_raw_resources:
            # print('Read from cache, instead of re-mounting.')
            self.resources = cache_mounted_resources
            self.resources_raw = cache_raw_resources
        else:
            # print('Building cache for mounted resources at {}'.format(Defaults.cache_dir))
            self._mount_references()

            if self.parse_it:
                self.cache.set('mounted_resources', self.resources)
                self.cache.set('resources_raw', self.resources_raw)

        self._distribute_providers()

        for _, resource in self.resources.items():
            self._expand_resource_tags(resource)

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
        if isinstance(resource.get('values', {}).get('tags'), list):
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
