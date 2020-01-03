from unittest import TestCase
from tests.mocks import MockedData, MockedWorld
from terraform_compliance.extensions.security_groups import SecurityGroup, SecurityGroupRule
from terraform_compliance.common.exceptions import Failure, TerraformComplianceInvalidData
from mock import patch


class TestSecurityGroupRule(TestCase):

    def setUp(self):
        self.rule_fields = ['cidr_blocks', 'from_port', 'to_port', 'protocol']

    def validate_rule(self, mocked_rule, rule):
        for field in self.rule_fields:
            self.assertEqual(mocked_rule[field],
                             rule.__getattribute__(field))

    def test_assign_sg_params_one_port_with_two_cidrs(self):
        self.validate_rule(MockedData.sg_params_ssh_with_2_cidrs,
                           SecurityGroupRule(**MockedData.sg_ssh_with_2_cidrs))

    def test_assign_sg_params_one_port_two_cidrs_any_proto(self):
        self.validate_rule(MockedData.sg_params_ssh_with_2_cidrs_any_proto,
                           SecurityGroupRule(**MockedData.sg_ssh_with_2_cidrs_any_proto))

    def test_assign_sg_params_all_ports_with_all_ips(self):
        self.validate_rule(MockedData.sg_params_all_port_all_ip,
                           SecurityGroupRule(**MockedData.sg_all_port_all_ip))

    def test_assign_sg_params_no_data_given_in_rules(self):
        self.validate_rule(MockedData.sg_params_all_port_no_ip,
                           SecurityGroupRule(**MockedData.sg_all_port_no_ip))

    def test_assign_sg_params_from_port_bigger_than_to_port(self):
        with self.assertRaises(TerraformComplianceInvalidData) as context:
            SecurityGroupRule(**MockedData.sg_invalid)

            self.assertTrue('Invalid configuration from_port can not be bigger than to_port.' in context.exception)

    # TODO: Implement failure tests here for consistency.


class TestSecurityGroup(TestCase):

    def setUp(self):
        self.sg_given = dict(
            port=80,
            protocol='tcp',
            cidr_blocks='0.0.0.0/0',
        )
        self.sg_in_conf = [
            dict(
                from_port=80,
                to_port=80,
                protocol='tcp',
                cidr_blocks=['0.0.0.0/0'],
                description='Test Security Group Description #1',
                values=dict(address='test.security_group_rule1')
            ),
            dict(
                from_port=81,
                to_port=81,
                protocol='tcp',
                cidr_blocks=['10.0.0.0/8', '192.168.0.0/24'],
                description='Test Security Group Description #2',
                values=dict(address='test.security_group_rule2')

            )
        ]

    # Tests about `must not have` scenarios
    # Checks are singular per security group rule, failures are imminent.
    def test_must_not_have_port_tcp_80_with_ALL_cidr(self):
        result, error = SecurityGroup(self.sg_given, self.sg_in_conf).validate()

        self.assertFalse(result)
        self.assertEqual('tcp/80 port is defined within 0.0.0.0/0 network in test.security_group_rule1.', error)

    def test_must_not_have_port_tcp_80_with_multi_cidr(self):
        self.sg_given['cidr_blocks'] = '192.168.1.0/24'
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/16', '0.0.0.0/0']

        result, error = SecurityGroup(self.sg_given, self.sg_in_conf).validate()

        self.assertFalse(result)
        self.assertEqual('tcp/80 port is defined within 192.168.0.0/16, 0.0.0.0/0 networks in '
                         'test.security_group_rule1.', error)

    def test_must_not_have_port_tcp_80_with_ALL_cidr_success(self):
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/16']
        self.assertTrue(SecurityGroup(self.sg_given, self.sg_in_conf).validate())

    def test_must_not_have_port_tcp_80_with_ALL_multi_success(self):
        self.sg_given['cidr_blocks'] = '192.168.1.0/16'
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/24', '10.0.0.0/8']
        self.assertTrue(SecurityGroup(self.sg_given, self.sg_in_conf).validate())

    def test_must_not_have_port_tcp_22_23_with_ALL_cidr(self):
        self.sg_given['port'] = '22-23'
        self.sg_in_conf[0]['from_port'] = 22
        self.sg_in_conf[0]['to_port'] = 23

        result, error = SecurityGroup(self.sg_given, self.sg_in_conf).validate()

        self.assertFalse(result)
        self.assertEqual('tcp/(22,23) ports are defined within 0.0.0.0/0 network in test.security_group_rule1.', error)

    def test_must_not_have_port_tcp_22_23_with_multi_cidr(self):
        self.sg_given['port'] = '22-23'
        self.sg_in_conf[0]['from_port'] = 22
        self.sg_in_conf[0]['to_port'] = 23
        self.sg_given['cidr_blocks'] = '192.168.1.0/24'
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/16', '0.0.0.0/0']

        result, error = SecurityGroup(self.sg_given, self.sg_in_conf).validate()

        self.assertFalse(result)
        self.assertEqual('tcp/(22,23) ports are defined within 192.168.0.0/16, 0.0.0.0/0 networks in '
                         'test.security_group_rule1.', error)

    def test_must_not_have_port_tcp_22_23_with_ALL_cidr_success(self):
        self.sg_given['port'] = '22-23'
        self.sg_in_conf[0]['from_port'] = 22
        self.sg_in_conf[0]['to_port'] = 23
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/16']
        self.assertTrue(SecurityGroup(self.sg_given, self.sg_in_conf).validate())

    def test_must_not_have_port_tcp_22_23_with_ALL_multi_success(self):
        self.sg_given['port'] = '22-23'
        self.sg_in_conf[0]['from_port'] = 22
        self.sg_in_conf[0]['to_port'] = 23
        self.sg_given['cidr_blocks'] = '192.168.1.0/16'
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/24', '10.0.0.0/8']
        self.assertTrue(SecurityGroup(self.sg_given, self.sg_in_conf).validate())

    def test_must_not_have_port_tcp_22_with_range_with_ALL_cidr(self):
        self.sg_given['port'] = '21-22'
        self.sg_in_conf[0]['from_port'] = 22
        self.sg_in_conf[0]['to_port'] = 23

        result, error = SecurityGroup(self.sg_given, self.sg_in_conf).validate()

        self.assertFalse(result)
        self.assertEqual('tcp/22 port is defined within 0.0.0.0/0 network in test.security_group_rule1.', error)

    def test_must_not_have_port_tcp_22_with_range_with_multi_cidr(self):
        self.sg_given['port'] = '21-22'
        self.sg_in_conf[0]['from_port'] = 22
        self.sg_in_conf[0]['to_port'] = 23
        self.sg_given['cidr_blocks'] = '192.168.1.0/24'
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/16', '0.0.0.0/0']

        result, error = SecurityGroup(self.sg_given, self.sg_in_conf).validate()

        self.assertFalse(result)
        self.assertEqual('tcp/22 port is defined within 192.168.0.0/16, 0.0.0.0/0 networks in '
                         'test.security_group_rule1.', error)

    def test_must_not_have_port_tcp_22_with_range_with_ALL_cidr_success(self):
        self.sg_given['port'] = '21-22'
        self.sg_in_conf[0]['from_port'] = 22
        self.sg_in_conf[0]['to_port'] = 23
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/16']
        self.assertTrue(SecurityGroup(self.sg_given, self.sg_in_conf).validate())

    def test_must_not_have_port_tcp_22_with_range_with_ALL_multi_success(self):
        self.sg_given['port'] = '21-22'
        self.sg_in_conf[0]['from_port'] = 22
        self.sg_in_conf[0]['to_port'] = 23
        self.sg_given['cidr_blocks'] = '192.168.1.0/16'
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/24', '10.0.0.0/8']
        self.assertTrue(SecurityGroup(self.sg_given, self.sg_in_conf).validate())

    # Tests about `must have` scenarios
    def test_must_have_port_tcp_443_with_ALL_cidr(self):
        self.sg_given['port'] = 443

        sg = SecurityGroup(self.sg_given, self.sg_in_conf)
        sg.must_have()
        result, error = sg.validate()

        self.assertFalse(result)
        self.assertEqual('tcp/443 port is not defined within 0.0.0.0/0 network in test_sg.', error)

    def test_must_have_port_tcp_443_with_multi_cidr(self):
        self.sg_given['port'] = 443
        self.sg_given['cidr_blocks'] = '192.168.1.0/24'
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/16', '0.0.0.0/0']

        sg = SecurityGroup(self.sg_given, self.sg_in_conf)
        sg.must_have()
        result, error = sg.validate()

        self.assertFalse(result)
        self.assertEqual('tcp/443 port is not defined within 192.168.1.0/24 network in test_sg.', error)

    def test_must_have_port_tcp_80_with_multi_cidr_success(self):
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/24']
        self.sg_in_conf[1]['cidr_blocks'] = ['192.168.1.0/24']
        self.sg_in_conf[1]['from_port'] = 79
        self.sg_in_conf[1]['to_port'] = 81
        self.sg_given['cidr_blocks'] = '192.168.0.0/24'

        sg = SecurityGroup(self.sg_given, self.sg_in_conf)
        sg.must_have()
        self.assertTrue(sg.validate())

    def test_must_have_port_tcp_80_with_multi_cidr_32_success(self):
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/24']
        self.sg_in_conf[1]['cidr_blocks'] = ['192.168.0.0/16']
        self.sg_in_conf[1]['from_port'] = 79
        self.sg_in_conf[1]['to_port'] = 81
        self.sg_given['cidr_blocks'] = '192.168.0.1/32'
        sg = SecurityGroup(self.sg_given, self.sg_in_conf)
        sg.must_have()
        self.assertTrue(sg.validate())

    @patch('radish.world', return_value=MockedWorld)
    def test_must_have_port_tcp_443_444_with_ALL_cidr(self, *args):
        self.sg_given['port'] = '443-444'

        sg = SecurityGroup(self.sg_given, self.sg_in_conf)
        sg.must_have()
        result, error = sg.validate()

        self.assertFalse(result)
        self.assertEqual('tcp/(443,444) ports are not defined within 0.0.0.0/0 network in test_sg.', error)

    def test_must_have_port_tcp_80_81_with_ALL_cidr(self):
        self.sg_given['port'] = '80-82'
        self.sg_in_conf[1]['cidr_blocks'] = ['0.0.0.0/0']

        sg = SecurityGroup(self.sg_given, self.sg_in_conf)
        sg.must_have()
        result, error = sg.validate()

        self.assertFalse(result)
        self.assertEqual('tcp/82 port is not defined within 0.0.0.0/0 network in test_sg.', error)

    # Tests about `must only have` scenarios
    # We are just checking if tcp/80 is defined for 0.0.0.0/0
    def test_must_only_have_port_tcp_80_with_ALL_cidr_success(self):
        sg = SecurityGroup(self.sg_given, self.sg_in_conf)
        sg.must_only_have()
        self.assertTrue(sg.validate())

    def test_must_only_have_port_tcp_80_81_with_ALL_cidr_success(self):
        self.sg_given['port'] = '80-81'

        sg = SecurityGroup(self.sg_given, self.sg_in_conf)
        sg.must_only_have()
        result, error = sg.validate()

        self.assertFalse(result)
        self.assertEqual('tcp/81 port is not defined within 0.0.0.0/0 network in test_sg.', error)

    def test_must_only_have_port_some_ports_are_over_configured(self):
        self.sg_in_conf[0]['from_port'] = 79
        self.sg_in_conf[0]['to_port'] = 81
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/16', '0.0.0.0/0']
        self.sg_in_conf[1]['from_port'] = 80
        self.sg_in_conf[1]['to_port'] = 80
        self.sg_in_conf[1]['cidr_blocks'] = ['0.0.0.0/0']

        sg = SecurityGroup(self.sg_given, self.sg_in_conf)
        sg.must_only_have()
        result, error = sg.validate()

        self.assertFalse(result)
        self.assertEqual('tcp/(81,79) ports are defined within 0.0.0.0/0 network in test_sg.', error)

    def test_must_only_have_port_not_match_multiple_errors_given(self):
        self.sg_in_conf[0]['from_port'] = 22
        self.sg_in_conf[0]['to_port'] = 23
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/16', '0.0.0.0/0']
        self.sg_in_conf[1]['from_port'] = 443
        self.sg_in_conf[1]['to_port'] = 444
        self.sg_in_conf[1]['cidr_blocks'] = ['0.0.0.0/0']

        sg = SecurityGroup(self.sg_given, self.sg_in_conf)
        sg.must_only_have()
        result, error = sg.validate()

        self.assertFalse(result)
        self.assertTrue('tcp/80 port is not defined within 0.0.0.0/0 network in test_sg.', error)
        self.assertTrue('tcp/(443,444,22,23) ports are defined within 0.0.0.0/0 network in test_sg.', error)
        self.assertTrue('None of the ports given defined within 0.0.0.0/0 network in test_sg.', error)

    def test_must_only_have_port_match_multiple_ports_not_ranges(self):
        self.sg_in_conf[0]['from_port'] = 22
        self.sg_in_conf[0]['to_port'] = 23
        self.sg_in_conf[0]['cidr_blocks'] = ['192.168.0.0/16', '0.0.0.0/0']
        self.sg_in_conf[1]['from_port'] = 443
        self.sg_in_conf[1]['to_port'] = 444
        self.sg_in_conf[1]['cidr_blocks'] = ['0.0.0.0/0']
        self.sg_given['ports'] = '22,23,443,444'

        sg = SecurityGroup(self.sg_given, self.sg_in_conf)
        sg.must_only_have()
        result, error = sg.validate()

        self.assertFalse(result)
        self.assertTrue('tcp/80 port is not defined within 0.0.0.0/0 network in test_sg.', error)
        self.assertTrue('tcp/(443,444,22,23) ports are defined within 0.0.0.0/0 network in test_sg.', error)
        self.assertTrue('None of the ports given defined within 0.0.0.0/0 network in test_sg.', error)
