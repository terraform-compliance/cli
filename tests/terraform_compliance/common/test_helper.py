from unittest import TestCase
from terraform_compliance.common.helper import (
    flatten_list,
    check_if_cidr,
    is_ip_in_cidr,
    assign_sg_params,
    validate_sg_rule,
    seek_key_in_dict,
    find_root_by_key,
    are_networks_same,
    convert_resource_type,
    seek_regex_key_in_dict_values,
    jsonify
)
from terraform_compliance.common.exceptions import Failure
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
        with self.assertRaises(Failure) as context:
            assign_sg_params(MockedData.sg_invalid)

            self.assertTrue('Invalid configuration from_port can not be bigger than to_port.' in context.exception)

    def test_validate_sg_rule_port_found_in_cidr(self):
        with self.assertRaises(Failure) as context:
            params = dict(from_port=22, to_port=22, cidr='0.0.0.0/0', ports='', proto='tcp')
            validate_sg_rule(MockedData.sg_params_all_port_all_ip, params, False)
            self.assertTrue('Found' in context.exception)

    def test_validate_sg_rule_invalid_port_range_within_scenario(self):
        with self.assertRaises(AssertionError) as context:
            params = dict(from_port=43, to_port=42, cidr=None, ports='', proto='tcp')
            validate_sg_rule(None, params, False)

            self.assertTrue('Port range is defined incorrectly within the Scenario.' in context.exception)

    def test_validate_sg_rule_port_range_found_in_cidr_fail(self):
        scenario_list = ['22-80', '21-22', '21-23', '70-72', '79-80', '79-81']
        for scenario in scenario_list:
            with self.assertRaises(Failure) as context:
                from_port, to_port = scenario.split('-')
                params = dict(proto='tcp', from_port=from_port, to_port=to_port, cidr='0.0.0.0/0', ports='')
                validate_sg_rule(MockedData.sg_params_list_range_public, params, False)
                self.assertTrue('Found' in context.exception)

    def test_validate_sg_rule_port_range_found_in_cidr_success_due_to_cidr_mismatch(self):
        scenario_list = ['22-80', '21-22', '21-23', '70-72', '79-80', '79-81']
        for scenario in scenario_list:
            from_port, to_port = scenario.split('-')
            params = dict(proto='tcp', from_port=from_port, to_port=to_port, ports='', cidr='0.0.0.0/0')
            self.assertTrue(validate_sg_rule(MockedData.sg_params_list_range_private, params, False))

    def test_validate_sg_rule_port_not_found_in_comma_delimited_scenario(self):
        with self.assertRaises(Failure) as context:
            ports = '22,443'.split(',')
            params = dict(proto='tcp', from_port=0, to_port=0, ports=ports, cidr='0.0.0.0/0')
            self.assertFalse(validate_sg_rule(MockedData.sg_params_list_range_public, params, True))

    def test_validate_sg_rule_port_found_in_comma_delimited_scenario(self):
        with self.assertRaises(Failure) as context:
            ports = range(22,80)
            ports = [str(i) for i in ports]
            params = dict(proto='tcp', from_port=0, to_port=0, ports=ports, cidr='0.0.0.0/0')
            self.assertFalse(validate_sg_rule(MockedData.sg_params_list_range_public, params, True))

    def test_seek_in_dict_finding_a_key_in_root(self):
        dictionary = dict(search_key=dict(something=[]))
        search_key = 'search_key'
        expected = [{'search_key': {'something': []}}]

        self.assertEqual(seek_key_in_dict(dictionary, search_key), expected)

    def test_seek_in_dict_finding_a_key_in_nested_dict(self):
        dictionary = dict(search_key=dict(something=dict(something_else=None)))
        search_key = 'something'
        expected = [{'something': {'something_else': None}}]

        self.assertEqual(seek_key_in_dict(dictionary, search_key), expected)

    def test_seek_in_dict_finding_multiple_keys_in_nested_dict(self):
        dictionary = dict(search_key=dict(something=dict(something_else=None, something=['something_else'])), something=[])
        search_key = 'something'
        expected = [{'something': {'something_else': None, 'something': ['something_else']}}, {'something': []}]

        self.assertEqual(seek_key_in_dict(dictionary, search_key), expected)

    def test_seek_in_dict_finding_values_in_non_dicts(self):
        dictionary = dict(search_key=dict(something=[]))
        search_key = 'something_else'
        expected = []

        self.assertEqual(seek_key_in_dict(dictionary, search_key), expected)

    def test_seek_in_dict_finding_values_in_non_dicts_on_root(self):
        dictionary = 'something_else'
        search_key = 'something_else'
        expected = []

        self.assertEqual(seek_key_in_dict(dictionary, search_key), expected)

    def test_find_root_by_key_single_return(self):
        haystack = dict(some_key=dict(values=dict(tags=[], something_else='something')))
        search_key = 'tags'
        expected = ['some_key']

        self.assertEqual(find_root_by_key(haystack, search_key), expected)

    def test_find_root_by_key_multiple_return(self):
        haystack = dict(some_key=dict(values=dict(tags=[], something_else='something')), other_key=dict(values=dict(tags=[], something_else='something')))
        search_key = 'tags'
        expected = ['other_key', 'some_key']

        self.assertEqual(sorted(find_root_by_key(haystack, search_key)), sorted(expected))

    def test_find_root_by_key_multiple_return_02(self):
        haystack = dict(some_key=dict(values=dict(tags=[], something_else='loki'), find_me='bingo'),
                        other_key=dict(values=dict(tags=[], something_else='thor'), find_me='b i n g o'))
        search_key = 'tags'
        return_key = 'find_me'
        expected = ['bingo', 'b i n g o']

        self.assertEqual(sorted(find_root_by_key(haystack, search_key, return_key)), sorted(expected))

    def test_are_networks_same_success(self):
        network_a = '192.168.0.0/24'
        networks = ['192.168.0.0/24']
        self.assertTrue(are_networks_same(network_a, networks))

    def test_are_networks_same_false(self):
        network_a = '192.168.0.0/24'
        networks = ['192.168.0.0/23']
        self.assertFalse(are_networks_same(network_a, networks))

    def test_convert_resource_type_success(self):
        self.assertEqual(convert_resource_type('AWS Security Group'), 'aws_security_group')

    def test_convert_resource_type_failure(self):
        self.assertEqual(convert_resource_type('test_resource'), 'test_resource')

    def test_seek_regex_in_dict_value_nested_dict(self):
        haystack = dict(search_key=dict(something='value'))
        key_name = 'something'
        needle = 'val.*'
        expected = ['value']

        self.assertEqual(seek_regex_key_in_dict_values(haystack, key_name, needle), expected)

    def test_jsonify(self):
        self.assertEqual(jsonify({}), {})
        self.assertEqual(jsonify([]), [])
        self.assertEqual(jsonify(12), 12)
        self.assertEqual(jsonify('something'), 'something')
        self.assertEqual(jsonify('{"test": "test_value"}'), {'test': 'test_value'})
