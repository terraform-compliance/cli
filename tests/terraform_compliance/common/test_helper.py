from unittest import TestCase
from terraform_compliance.common.helper import flatten_list, check_port_cidr_ranges
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

    def test_check_port_cidr_ranges_port_fail(self):
        pass

    def test_check_port_cidr_ranges_port_passed_because_of_different_protocol(self):
        pass

    def test_check_port_cidr_ranges_port_fail_and_protocol_number_is_used(self):
        pass

    def test_check_port_cidr_ranges_port_not_fail_because_of_cidr(self):
        pass

    def test_check_port_cidr_ranges_port_fail_because_of_given_ip_is_a_member_of_cidr(self):
        pass
