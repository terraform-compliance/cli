from unittest import TestCase
from terraform_compliance.common.helper import (
    flatten_list,
    assign_sg_params,
    validate_sg_rule
)
from tests.mocks import MockedData
from copy import deepcopy


class TestHelperFunctions(TestCase):

    def test_flatten_single_dimensional_list(self):
        a = ['a', 'b', 'c']
        b = ['a', 'b', 'c']

        self.assertEqual(flatten_list(a), b)

    def test_flatten_multi_dimensional_list(self):
        a = ['a', 'b', ['c']]
        b = ['a', 'b', 'c']

        self.assertEqual(flatten_list(a), b)

    def test_flatten_multi_dimensional_nested_list(self):
        a = ['a', 'b', ['c', ['d', 'e'], 'f'], 'g', 'h', 'i', ['j', 'k']]
        b = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']

        self.assertEqual(flatten_list(a), b)

    def test_assign_sg_params_one_port_with_two_cidrs(self):
        self.assertEqual(MockedData.sg_params_ssh_with_2_cidrs, assign_sg_params(MockedData.sg_ssh_with_2_cidrs))

    def test_assign_sg_params_one_port_two_cidrs_any_proto(self):
        self.assertEqual(MockedData.sg_params_ssh_with_2_cidrs_any_proto, assign_sg_params(MockedData.sg_ssh_with_2_cidrs_any_proto))

    def test_assign_sg_params_all_ports_with_all_ips(self):
        self.assertEqual(MockedData.sg_params_all_port_all_ip, assign_sg_params(MockedData.sg_all_port_all_ip))

    def test_assign_sg_params_no_data_given_in_rules(self):
        self.assertEqual(MockedData.sg_params_all_port_no_ip, assign_sg_params(MockedData.sg_all_port_no_ip))

    def test_assign_sg_params_from_port_bigger_than_to_port(self):
        with self.assertRaises(AssertionError) as context:
            assign_sg_params(MockedData.sg_invalid)

            self.assertTrue('Invalid configuration from_port can not be bigger than to_port.' in context.exception)

    def test_validate_sg_rule_port_found_in_cidr(self):
        with self.assertRaises(AssertionError) as context:
            validate_sg_rule('tcp', '22', '0.0.0.0/0', MockedData.sg_params_all_port_all_ip)

            self.assertTrue('Found' in context.exception)

    def test_validate_sg_rule_port_found_but_cidr_is_different(self):
        pass

    def test_validate_sg_rule_port_found_but_proto_is_different(self):
        pass

    def test_check_sg_rules_fail(self):
        pass

    def test_check_sg_rules_passed_because_of_different_protocol(self):
        pass

    def test_check_sg_rules_fail_and_protocol_number_is_used(self):
        pass

    def test_check_sg_rules_not_fail_because_of_cidr(self):
        pass

    def test_check_sg_rules_fail_because_of_given_ip_is_a_member_of_cidr(self):
        pass
