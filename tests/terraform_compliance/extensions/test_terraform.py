from unittest import TestCase
from terraform_compliance.extensions.terraform import TerraformParser, seek_key_in_dict
from tests.mocks import MockedData
from mock import patch

class TestTerraformParser(TestCase):


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_version_check_success(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['format_version'] = obj.supported_format_versions[0]
        obj.raw['terraform_version'] = obj.supported_terraform_versions[0]
        self.assertTrue(obj._version_check())


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_version_check_failure_unsupported_format_version(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['format_version'] = 'some_unsupported_format_version'
        obj.raw['terraform_version'] = obj.supported_terraform_versions[0]
        with self.assertRaises(SystemExit):
            obj._version_check()


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_version_check_failure_unsupported_terraform_version(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['format_version'] = obj.supported_format_versions[0]
        obj.raw['terraform_version'] = 'some_unsupported_terraform_version'
        with self.assertRaises(SystemExit):
            obj._version_check()


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_identify_data_file_success(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['values'] = True
        obj._identify_data_file()
        self.assertEqual(obj.file_type, 'state')


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_identify_data_file_failure(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj._identify_data_file()
        self.assertEqual(obj.file_type, 'plan')


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_variables(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['variables'] = True
        obj._parse_variables()
        self.assertEqual(obj.variables, True)


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_plan_data(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['planned_values'] = {
            'root_module': {
                'resources': [
                    {
                        'address': 'data_something'
                    }
                ]
            }
        }
        obj._parse_resources()
        self.assertEqual(obj.data['data_something'], {'address': 'data_something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_plan_resource(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['planned_values'] = {
            'root_module': {
                'resources': [
                    {
                        'address': 'something'
                    }
                ]
            }
        }
        obj._parse_resources()
        self.assertEqual(obj.resources['something'], {'address': 'something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_state_data(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['values'] = {
            'root_module': {
                'resources': [
                    {
                        'address': 'data_something'
                    }
                ]
            }
        }
        obj._parse_resources()
        self.assertEqual(obj.data['data_something'], {'address': 'data_something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_state_resource(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['values'] = {
            'root_module': {
                'resources': [
                    {
                        'address': 'something'
                    }
                ]
            }
        }
        obj._parse_resources()
        self.assertEqual(obj.resources['something'], {'address': 'something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_child_resources_exists_in_the_state_data(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['values'] = {
            'root_module': {
                'child_modules': {
                    'resources': [
                        {
                            'address': 'data_something'
                        }
                    ]
                }
            }
        }
        obj._parse_resources()
        self.assertEqual(obj.data['data_something'], {'address': 'data_something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_child_resources_exists_in_the_state_resource(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['values'] = {
            'root_module': {
                'child_modules': {
                    'resources': [
                        {
                            'address': 'something'
                        }
                    ]
                }
            }
        }
        obj._parse_resources()
        self.assertEqual(obj.resources['something'], {'address': 'something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_configurations_resources(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['configuration'] = {
            'root_module': {
                'resources': [
                    {
                        'address': 'something'
                    }
                ]
            }
        }
        obj._parse_configurations()
        self.assertEqual(obj.configuration['resources']['something'], {'address': 'something'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_configurations_variables(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['configuration'] = {
            'root_module': {
                'variables': [
                    {
                        'variable_key': 'variable_value'
                    }
                ]
            }
        }
        obj._parse_configurations()
        self.assertEqual(obj.configuration['variables'], [{'variable_key': 'variable_value'}])


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_configurations_providers(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['configuration'] = {
            'provider_config': {
                'some_provider': 'some_provider_data'
            }
        }
        obj._parse_configurations()
        self.assertEqual(obj.configuration['providers'], {'some_provider': 'some_provider_data'})


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_mount_resources_with_ref_type(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        target = 'target_ref'
        source = 'source_ref'
        ref_type = 'some_key'
        obj.resources = {
            target: {
                'values': {
                    'some_key': ['a']
                }
            },
            source: {
                'values': {
                    'some_key': 'some_value'
                }
            }
        }
        obj._mount_resources([source], [target], ref_type)
        self.assertEqual(['a', {'some_key': 'some_value'}], obj.resources[target]['values'][ref_type])


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_mount_resources_without_ref_type(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        target = 'target_ref'
        source = 'source_ref'
        ref_type = 'some_ref'
        obj.resources = {
            target: {
                'values': {}
            },
            source: {
                'values': {
                    'some_key': 'some_value'
                }
            }
        }
        obj._mount_resources([source], [target], ref_type)
        self.assertEqual([{'some_key': 'some_value'}], obj.resources[target]['values'][ref_type])


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resource_from_name_resource_name_in_resources(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.resources = {'something': True}
        self.assertEqual(obj._find_resource_from_name('something'), ['something'])


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resource_from_name_resource_name_in_child_resources(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.resources = {
            'a': {
                'type': 'resource_type',
                'name': 'resource_id'
            }
        }
        self.assertEqual(obj._find_resource_from_name('resource_type.resource_id'), ['a'])

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_distribute_providers(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.resources = {
            'provider_resource_id': {
                'type': 'resource_type',
                'name': 'resource_id'
            },
            'other-provider_other_resource_id': {
                'type': 'other-provider_other_resource_type',
                'name': 'resource_id'
            }
        }
        obj._distribute_providers()

        print(obj.providers)
        self.assertTrue('provider' in obj.providers)
        self.assertTrue('other-provider' in obj.providers)

    @patch.object(TerraformParser, '_read_file', return_value={})
    @patch.object(TerraformParser, '_version_check', return_value=None)
    @patch.object(TerraformParser, '_identify_data_file', return_value=None)
    @patch.object(TerraformParser, '_parse_resources', return_value=None)
    @patch.object(TerraformParser, '_parse_configurations', return_value=None)
    @patch.object(TerraformParser, '_mount_references', return_value=None)
    @patch.object(TerraformParser, '_distribute_providers', return_value=None)
    def test_parse_plan(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['variables'] = True
        obj.parse()

        self.assertEqual(obj.variables, True)

    @patch.object(TerraformParser, '_read_file', return_value={})
    @patch.object(TerraformParser, '_version_check', return_value=None)
    @patch.object(TerraformParser, '_identify_data_file', return_value=None)
    @patch.object(TerraformParser, '_parse_resources', return_value=None)
    @patch.object(TerraformParser, '_parse_configurations', return_value=None)
    @patch.object(TerraformParser, '_mount_references', return_value=None)
    @patch.object(TerraformParser, '_distribute_providers', return_value=None)
    def test_parse_state(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.raw['variables'] = True
        obj.file_type = 'state'
        obj.parse()

        self.assertEqual(obj.variables, None)


    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resources_by_type_success(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.resources = {
            'provider_resource_id': {
                'type': 'resource_type',
                'name': 'resource_id'
            },
            'other-provider_other_resource_id': {
                'type': 'other-provider_other_resource_type',
                'name': 'resource_id'
            }
        }

        self.assertEqual(obj.find_resources_by_type('resource_type'),
                         [{
                            'type': 'resource_type',
                            'name': 'resource_id'
                          }])

    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resources_by_type_failure(self, *args):
        obj = TerraformParser('somefile', parse_it=False)
        obj.resources = {
            'provider_resource_id': {
                'type': 'resource_type',
                'name': 'resource_id'
            },
            'other-provider_other_resource_id': {
                'type': 'other-provider_other_resource_type',
                'name': 'resource_id'
            }
        }

        self.assertEqual(obj.find_resources_by_type('invalid_resource'),
                         [])
