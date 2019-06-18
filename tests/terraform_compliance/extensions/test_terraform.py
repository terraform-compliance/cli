from unittest import TestCase
from terraform_compliance.extensions.terraform import TerraformParser, seek_key_in_dict
from tests.mocks import MockedData
from mock import patch

class TestTerraformParser(TestCase):

    @patch.object(TerraformParser, '_read_file', return_value=MockedData.mocked_plan_outputs['security_group_mounting'])
    def test_security_group_mounting_success(self, *args):
            obj = TerraformParser('somefile')
            self.assertTrue('ingress' in obj.resources['aws_security_group.example']['values'])

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_version_check_success(self, *args):
        obj = TerraformParser('somefile')
        obj.raw['format_version'] = obj.supported_format_versions[0]
        obj.raw['terraform_version'] = obj.supported_terraform_versions[0]
        self.assertTrue(obj._version_check())

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_version_check_failure_unsupported_format_version(self, *args):
        obj = TerraformParser('somefile')
        obj.raw['format_version'] = 'some_unsupported_format_version'
        obj.raw['terraform_version'] = obj.supported_terraform_versions[0]
        with self.assertRaises(SystemExit):
            obj._version_check()

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_version_check_failure_unsupported_terraform_version(self, *args):
        obj = TerraformParser('somefile')
        obj.raw['format_version'] = obj.supported_format_versions[0]
        obj.raw['terraform_version'] = 'some_unsupported_terraform_version'
        with self.assertRaises(SystemExit):
            obj._version_check()

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_identify_data_file_success(self, *args):
        obj = TerraformParser('somefile')
        obj.raw['values'] = True
        obj._identify_data_file()
        self.assertEqual(obj.file_type, 'state')

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_identify_data_file_failure(self, *args):
        obj = TerraformParser('somefile')
        obj._identify_data_file()
        self.assertEqual(obj.file_type, 'plan')

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_variables(self, *args):
        obj = TerraformParser('somefile')
        obj.raw['variables'] = True
        obj._parse_variables()
        self.assertEqual(obj.variables, True)

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_plan_data(self, *args):
        obj = TerraformParser('somefile')
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

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_plan_resource(self, *args):
        obj = TerraformParser('somefile')
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

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_state_data(self, *args):
        obj = TerraformParser('somefile')
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

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_resources_exists_in_the_state_resource(self, *args):
        obj = TerraformParser('somefile')
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

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_child_resources_exists_in_the_state_data(self, *args):
        obj = TerraformParser('somefile')
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

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_resources_child_resources_exists_in_the_state_resource(self, *args):
        obj = TerraformParser('somefile')
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

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_configurations_resources(self, *args):
        obj = TerraformParser('somefile')
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

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_configurations_variables(self, *args):
        obj = TerraformParser('somefile')
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

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_configurations_providers(self, *args):
        obj = TerraformParser('somefile')
        obj.raw['configuration'] = {
            'provider_config': {
                'some_provider': 'some_provider_data'
            }
        }
        obj._parse_configurations()
        self.assertEqual(obj.configuration['providers'], {'some_provider': 'some_provider_data'})

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_mount_respources_with_ref_type(self, *args):
        self.assertTrue(False)

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_mount_respources_without_ref_type(self, *args):
        self.assertTrue(False)

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resource_from_name_resource_name_in_resources(self, *args):
        self.assertTrue(False)

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resource_from_name_resource_name_in_child_resources(self, *args):
        self.assertTrue(False)

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_mount_references(self, *args):
        # TODO: Extend this
        self.assertTrue(False)

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_distribute_providers(self, *args):
        # TODO: Extend this
        self.assertTrue(False)

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_plan(self, *args):
        self.assertTrue(False)

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_parse_state(self, *args):
        self.assertTrue(False)

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resources_by_type_success(self, *args):
        self.assertTrue(False)

    @patch.object(TerraformParser, 'parse', return_value=None)
    @patch.object(TerraformParser, '_read_file', return_value={})
    def test_find_resources_by_type_failure(self, *args):
        self.assertTrue(False)
