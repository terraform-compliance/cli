from unittest import TestCase
from terraform_compliance.extensions.terraform_validate import enable_resource_mounting
from terraform_compliance.extensions.terraform_validate import _change_value_in_dict
from tests.mocks import MockedData
from copy import deepcopy
from mock import patch


class TestTerraformValidate(TestCase):

    def test_change_value_in_dict_path_to_value_is_str(self):
        target_dictionary = deepcopy(MockedData.target_dictionary)
        _change_value_in_dict(target_dictionary,
                              MockedData.path_to_change_as_string,
                              MockedData.target_value)
        self.assertEqual(target_dictionary, MockedData.expected_target_dictionary)

    def test_change_value_in_dict_path_to_value_is_list(self):
        target_dictionary = deepcopy(MockedData.target_dictionary)
        _change_value_in_dict(target_dictionary,
                              MockedData.path_to_change_as_list,
                              MockedData.target_value)
        self.assertEqual(target_dictionary, MockedData.expected_target_dictionary)

    def test_enable_resource_mounting_success(self):
        mocked_tf = deepcopy(MockedData.mocked_tf_conf_for_mounting)
        enable_resource_mounting(mocked_tf)
        expected_target = MockedData.expected_tf_conf_for_mounting['resource']['aws_security_group']['test_instance']
        self.assertTrue('test_ingress' in expected_target)
        self.assertTrue('test_egress' in expected_target)
        self.assertTrue('default' in MockedData.expected_tf_conf_for_mounting['resource']['aws_security_group'])

    def test_enable_resource_mounting_success_while_there_is_no_mounting(self):
        mocked_tf = deepcopy(MockedData.mocked_tf_conf_with_no_mounting)
        enable_resource_mounting(mocked_tf)
        expected_target = MockedData.mocked_tf_conf_with_no_mounting['resource']['aws_security_group']['test_instance']
        self.assertFalse('test_ingress' in expected_target)
        self.assertFalse('test_egress' in expected_target)
        self.assertTrue('default' in MockedData.mocked_tf_conf_with_no_mounting['resource']['aws_security_group'])
