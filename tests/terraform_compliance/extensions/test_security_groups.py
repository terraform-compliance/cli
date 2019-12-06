from unittest import TestCase
from tests.mocks import MockedData
from terraform_compliance.extensions.security_groups import SecurityGroup, SecurityGroupRule
from terraform_compliance.common.exceptions import Failure, TerraformComplianceInvalidData


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


class TestSecurityGroup(TestCase):
