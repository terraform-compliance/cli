from unittest import TestCase
from terraform_compliance.common.helper import (
    flatten_list,
    generate_target_resource,
    expand_variable,
    check_if_cidr,
    is_ip_in_cidr,
    assign_sg_params,
    validate_sg_rule,
    change_value_in_dict
)
from tests.mocks import MockedData


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

    def test_generate_target_resource(self):
        self.assertEqual(['resource', 'target', 'test'], generate_target_resource('target.test'))

    def test_generate_target_resource_has_id_and_name_in_it(self):
        self.assertEqual(['resource', 'target', 'test'], generate_target_resource('target.test.id'))
        self.assertEqual(['resource', 'target', 'test'], generate_target_resource('target.test.name'))

    def test_expand_variable_found(self):
        tf_conf = dict(variable=dict(key='value'))
        self.assertEqual('value', expand_variable(tf_conf, '${var.key}'))

    def test_expand_variable_not_found(self):
        tf_conf = dict(variable=dict(key='value'))
        self.assertEqual('${var.invalid_key}', expand_variable(tf_conf, '${var.invalid_key}'))
        self.assertEqual('${invalid.invalid_key}', expand_variable(tf_conf, '${invalid.invalid_key}'))

    def test_check_if_cidr_success(self):
        self.assertTrue(check_if_cidr('10.0.0.0/8'))
        self.assertTrue(check_if_cidr('10.14.0.0/16'))
        self.assertTrue(check_if_cidr('10.0.0.0/24'))
        self.assertTrue(check_if_cidr('10.0.0.7/32'))

    def test_check_if_cidr_failure(self):
        self.assertFalse(check_if_cidr('256.0.0.0/8'))
        self.assertFalse(check_if_cidr('10.256.0.0/16'))
        self.assertFalse(check_if_cidr('10.0.256.0/24'))
        self.assertFalse(check_if_cidr('10.0.0.256/32'))
        self.assertFalse(check_if_cidr('10.0.0.256/33'))

    def test_is_ip_in_cidr_success(self):
        self.assertTrue(is_ip_in_cidr('10.0.0.0/8', ['0.0.0.0/0']))
        self.assertTrue(is_ip_in_cidr('10.0.0.0/16', ['10.0.0.0/8']))
        self.assertTrue(is_ip_in_cidr('10.0.200.0/24', ['10.0.0.0/16']))
        self.assertTrue(is_ip_in_cidr('10.0.0.1/32', ['10.0.0.0/24']))

    def test_is_ip_in_cidr_failure(self):
        self.assertFalse(is_ip_in_cidr('200.0.0.0/16', ['10.0.0.0/8']))
        self.assertFalse(is_ip_in_cidr('10.200.0.0/24', ['10.0.0.0/16']))
        self.assertFalse(is_ip_in_cidr('10.0.1.1/32', ['10.0.0.0/24']))

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
            validate_sg_rule(False, 'tcp', '22', '22', '', '0.0.0.0/0', MockedData.sg_params_all_port_all_ip)
            self.assertTrue('Found' in context.exception)

    def test_change_value_in_dict_with_str_path(self):
        target_dict = dict(key=dict(another_key='value'))
        change_value_in_dict(target_dict, 'key', dict(added_key='added_value'))
        self.assertEqual(target_dict, dict(key=dict(another_key='value', added_key='added_value')))

    def test_change_value_in_dict_with_dict_path(self):
        target_dict = dict(key=dict(another_key='value'))
        change_value_in_dict(target_dict, ['key'], dict(added_key='added_value'))
        self.assertEqual(target_dict, dict(key=dict(another_key='value', added_key='added_value')))

    def test_validate_sg_rule_invalid_port_range_within_scenario(self):
        with self.assertRaises(AssertionError) as context:
            validate_sg_rule(False, 'tcp', '43', '42', '', None, None)

            self.assertTrue('Port range is defined incorrectly within the Scenario.' in context.exception)

    def test_validate_sg_rule_port_range_found_in_cidr_fail(self):
        scenario_list = ['22-80', '21-22', '21-23', '70-72', '79-80', '79-81']
        for scenario in scenario_list:
            with self.assertRaises(AssertionError) as context:
                from_port, to_port = scenario.split('-')
                validate_sg_rule(False, 'tcp', from_port, to_port, '', '0.0.0.0/0', MockedData.sg_params_list_range_public)
                self.assertTrue('Found' in context.exception)

    def test_validate_sg_rule_port_range_found_in_cidr_success_due_to_cidr_mismatch(self):
        scenario_list = ['22-80', '21-22', '21-23', '70-72', '79-80', '79-81']
        for scenario in scenario_list:
            from_port, to_port = scenario.split('-')
            self.assertTrue(validate_sg_rule(False, 'tcp', from_port, to_port, '', '0.0.0.0/0',
                                             MockedData.sg_params_list_range_private))

    def test_validate_sg_rule_port_not_found_in_comma_delimited_scenario(self):
        with self.assertRaises(AssertionError) as context:
            ports = '22,443'.split(',')
            self.assertFalse(validate_sg_rule(True, 'tcp', '0', '0', ports, '0.0.0.0/0', MockedData.sg_params_list_range_public))

    def test_validate_sg_rule_port_found_in_comma_delimited_scenario(self):
        with self.assertRaises(AssertionError) as context:
            ports = range(22,80)
            ports = [str(i) for i in ports]
            self.assertFalse(validate_sg_rule(True, 'tcp', '0', '0', ports, '0.0.0.0/0', MockedData.sg_params_list_range_public))
