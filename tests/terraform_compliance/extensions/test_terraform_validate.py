from unittest import TestCase
from terraform_compliance.extensions.terraform_validate import enable_resource_mounting
from terraform_compliance.extensions.terraform_validate import change_value_in_dict
from tests.mocks import MockedData
from copy import deepcopy


class TestTerraformValidate(TestCase):

    def test_change_value_in_dict_path_to_value_is_str(self):
        target_dictionary = deepcopy(MockedData.target_dictionary)
        change_value_in_dict(target_dictionary,
                             MockedData.path_to_change_as_string,
                             MockedData.target_value)
        self.assertEqual(target_dictionary, MockedData.expected_target_dictionary)

    def test_change_value_in_dict_path_to_value_is_list(self):
        target_dictionary = deepcopy(MockedData.target_dictionary)
        change_value_in_dict(target_dictionary,
                             MockedData.path_to_change_as_list,
                             MockedData.target_value)
        self.assertEqual(target_dictionary, MockedData.expected_target_dictionary)

    def test_enable_resource_mounting_success(self):
        mocked_tf = deepcopy(MockedData.mocked_tf_conf_for_mounting)
        enable_resource_mounting(mocked_tf)

        self.assertTrue('test_ingress' in mocked_tf['resource']['aws_security_group']['test_instance'])
        self.assertTrue('test_egress' in mocked_tf['resource']['aws_security_group']['test_instance'])
        self.assertTrue('default' in MockedData.expected_tf_conf_for_mounting['resource']['aws_security_group'])

    def test_enable_resource_mounting_success_while_there_is_no_mounting(self):
        mocked_tf = deepcopy(MockedData.mocked_tf_conf_with_no_mounting)
        enable_resource_mounting(mocked_tf)

        self.assertFalse('test_ingress' in mocked_tf['resource']['aws_security_group']['test_instance'])
        self.assertFalse('test_egress' in mocked_tf['resource']['aws_security_group']['test_instance'])
        self.assertTrue('default' in MockedData.mocked_tf_conf_with_no_mounting['resource']['aws_security_group'])

    def test_check_if_ingress_egress_is_created(self):
        mocked_tf = deepcopy(MockedData.mocked_tf_conf_for_mounting)
        enable_resource_mounting(mocked_tf)

        self.assertTrue('ingress' in mocked_tf['resource']['aws_security_group']['test_instance'])
        self.assertTrue(type(mocked_tf['resource']['aws_security_group']['test_instance']['ingress']) is list)
        self.assertTrue('egress' in mocked_tf['resource']['aws_security_group']['test_instance'])
        self.assertTrue(type(mocked_tf['resource']['aws_security_group']['test_instance']['egress']) is list)
        self.assertTrue('default' in MockedData.expected_tf_conf_for_mounting['resource']['aws_security_group'])
