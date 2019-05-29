import json


class TerraformParser(object):
    def __init__(self, filename):
        '''
        This class reads the given terraform plan filename ( in json format ) and assigns required variables for
        further steps in terraform-compliance. If the file is not a json or terraform plan file, then it will be
        checked and exited in prior steps.

        :param filename: terraform plan filename in json format.
        '''
        self.data = self._read_file(filename)
        self.variables = None
        self.resources = dict()
        self.configuration = dict(resources=dict(), variables=dict())
        self.parse()

    def _read_file(self, filename):
        '''
        Reads the json filename as a dictionary. We are not checking if the file is a json file again, since
        it is already checked in main.py

        :param filename: json filename with full path
        :return: parsed dictionary
        '''
        with open(filename, 'r') as plan_file:
            data = json.load(plan_file)

        return data

    def _parse_variables(self):
        '''
        Assignes all variables that is defined within the terraform plan

        :return: none
        '''
        self.variables = self.data.get('variables', None)

    def _parse_resources(self):
        '''
        Assigns all resources defined in the terraform plan

        :return: none
        '''
        for resource_name in self.data['planned_values']['root_module'].get('resources',dict()):
            self.resources[resource_name['address']] = resource_name

    def _parse_configurations(self):
        '''
        Assigns all configuration related data defined in the terraform plan. This is mostly used for
        resources referencing each other.

        :return: none
        '''
        for configuration_name in self.data['configuration']['root_module'].get('resources', dict()):
            self.configuration['resources'][configuration_name['address']] = configuration_name

        self.configuration['variagbles'] = self.data['configuration']['root_module'].get('variables', dict())

    def _mount_resources(self, source, target, ref_type):
        '''
        Mounts values of the source resource to the target resource's values with ref_type key

        :param source: source resource
        :param target:  target resource
        :param ref_type: reference type (e.g. ingress )
        :return: none
        '''
        for source_resource in source:
            for target_resource in target:
                if ref_type not in self.resources[target_resource]['values']:
                    print('New ref_type added to {} : {}'.format(target_resource, ref_type))
                    self.resources[target_resource]['values'][ref_type] = list()
                    self.resources[target_resource]['values'][ref_type].append(self.resources[source_resource]['values'])
                else:
                    print('Extended ref_type to {} : {}'.format(target_resource, ref_type))
                    self.resources[target_resource]['values'][ref_type].append(self.resources[source_resource]['values'])

    def _find_resource_from_name(self, resource_name):
        '''
        Finds all the resources that is starting with resource_name

        :param resource_name: The first initials of the resource
        :return: list of the found resources
        '''
        if resource_name in self.resources:
            return [resource_name]

        resource_list = list()

        for key, value in self.resources.items():
            if key.startswith(resource_name):
                resource_list.append(key)

        return resource_list

    def _mount_references(self):
        '''
        Find the references that is defined in self.configuration
        :return:
        '''
        invalid_references = ('var')
        for resource in self.configuration['resources']:
            if 'expressions' in self.configuration['resources'][resource]:
                ref_list = list()
                for key, value in self.configuration['resources'][resource]['expressions'].items():
                    if 'references' in value:
                        ref_list.extend([ref for ref in value['references'] if not ref.startswith(invalid_references)])

                ref_type = self.configuration['resources'][resource]['expressions']['type']['constant_value']

                source_resources = self._find_resource_from_name(self.configuration['resources'][resource]['address'])
                self._mount_resources(source_resources, ref_list, ref_type)

    def parse(self):
        '''
        Main method for initialising the parsing of the terraform plan json file

        :return: nothing
        '''
        self._parse_variables()
        self._parse_resources()
        self._parse_configurations()
        self._mount_references()
