from unittest import TestCase
from terraform_compliance.steps.steps import (
    i_have_name_section_configured,
    i_action_them,
    i_expect_the_result_is_operator_than_number,
    it_condition_contain_something,
    encryption_is_enabled,
    its_value_condition_match_the_search_regex_regex,
    it_condition_have_proto_protocol_and_port_port_for_cidr,
    it_fails
)
from terraform_compliance.common.exceptions import TerraformComplianceNotImplemented, Failure, TerraformComplianceInternalFailure
from tests.mocks import MockedStep, MockedWorld, MockedTerraformPropertyList, MockedTerraformResourceList, MockedTerraformResource
from mock import patch


class Test_Step_Cases(TestCase):

    def test_i_have_name_section_configured_type_not_found(self):
        step = MockedStep()
        with self.assertRaises(AssertionError) as err:
            i_have_name_section_configured(step, 'some_name', 'some_invalid_type', 'some_world')

        self.assertEqual(str(err.exception), 'some_invalid_type configuration type does not exist or not implemented '
                                             'yet. Use resource(s), provider(s), variable(s) or data(s) instead.')

    def test_i_have_name_section_configured_resource_that_supports_tags_found(self):
        step = MockedStep()
        world = MockedWorld()
        name = 'resource that supports tags'
        type_name = 'resource'

        self.assertTrue(i_have_name_section_configured(step, name, type_name, world))
        self.assertEqual(step.context.name, name)
        self.assertEqual(step.context.type, type_name)

    def test_i_have_name_section_configured_resource_that_supports_tags_not_found(self):
        step = MockedStep()
        world = MockedWorld()
        del world.config.terraform.resources['provider_type_id']
        name = 'resource that supports tags'
        type_name = 'resource'

        self.assertIsNone(i_have_name_section_configured(step, name, type_name, world))
        self.assertEqual(step.state, 'skipped')

    def test_i_have_name_section_configured_resource_not_found(self):
        step = MockedStep()
        world = MockedWorld()
        name = 'non_existent_resource_id'
        type_name = 'resource'

        self.assertIsNone(i_have_name_section_configured(step, name, type_name, world))
        self.assertEqual(step.state, 'skipped')

    def test_i_have_name_section_configured_resource_found(self):
        step = MockedStep()
        world = MockedWorld()
        name = 'resource_type_without_tags'
        type_name = 'resource'

        self.assertTrue(i_have_name_section_configured(step, name, type_name, world))

    def test_i_have_name_section_configured_variable_not_found(self):
        step = MockedStep()
        world = MockedWorld()
        name = 'non_existent_variable'
        type_name = 'variable'

        self.assertIsNone(i_have_name_section_configured(step, name, type_name, world))
        self.assertEqual(step.state, 'skipped')

    def test_i_have_name_section_configured_variable_found(self):
        step = MockedStep()
        world = MockedWorld()
        name = 'some_variable'
        type_name = 'variables'

        self.assertTrue(i_have_name_section_configured(step, name, type_name, world))

    def test_i_have_name_section_configured_provider_not_found(self):
        step = MockedStep()
        world = MockedWorld()
        name = 'non_existing_provider'
        type_name = 'provider'

        self.assertIsNone(i_have_name_section_configured(step, name, type_name, world))
        self.assertEqual(step.state, 'skipped')

    def test_i_have_name_section_configured_provider_found(self):
        step = MockedStep()
        world = MockedWorld()
        name = 'some_provider'
        type_name = 'providers'

        self.assertTrue(i_have_name_section_configured(step, name, type_name, world))

    def test_it_condition_contain_something_resource_is_not_dict_failure(self):
        step = MockedStep()
        step.context_sensitive_sentence = 'it must contain something'
        step.context.type = 'resource'
        step.context.stash = ['some_resource']
        with self.assertRaises(Failure):
            self.assertIsNone(it_condition_contain_something(step, 'something'))

    def test_it_condition_contain_something_resource_not_found(self):
        step = MockedStep()
        step.context_sensitive_sentence = 'it must contain something'
        step.context.type = 'resource'
        step.context.stash = [
            {
                'address': 'some_address',
                'type': 'resource',
                'values': {
                    'something': True
                }
            }
        ]
        with self.assertRaises(Failure) as err:
            self.assertIsNone(it_condition_contain_something(step, 'something else'))
        self.assertEqual(str(err.exception), '{} ({}) does not have {} property.'.format('some_address',
                                                                                         'resource',
                                                                                         'something else'))

    @patch('terraform_compliance.extensions.ext_radish_bdd', return_value=None)
    def test_it_condition_contain_something_resource_not_found_skip_step(self, *args):
        step = MockedStep()
        step.context_sensitive_sentence = 'it contains something'
        step.context.type = 'resource'
        step.context.stash = [
            {
                'address': 'some_address',
                'type': 'resource',
                'values': {
                    'something': True
                }
            }
        ]

        self.assertIsNone(it_condition_contain_something(step, 'something else'))

    def test_it_condition_contain_something_resource_found(self):
        step = MockedStep()
        step.context_sensitive_sentence = 'it contains something'
        step.context.type = 'resource'
        step.context.stash = [
            {
                'address': 'some_address',
                'type': 'resource',
                'values': {
                    'something': True
                }
            }
        ]

        self.assertTrue(it_condition_contain_something(step, 'something'))

    def test_it_condition_contain_something_resource_value_is_list(self):
        step = MockedStep()
        step.context_sensitive_sentence = 'it contains something'
        step.context.type = 'resource'
        step.context.stash = [
            {
                'address': 'some_address',
                'type': 'resource',
                'values': [
                    {
                        'key': 'something',
                        'value': 'some_value'
                    }
                ]
            }
        ]

        self.assertTrue(it_condition_contain_something(step, 'something'))

    def test_it_condition_contain_something_resource_value_is_list_but_invalid(self):
        step = MockedStep()
        step.context_sensitive_sentence = 'it contains something'
        step.context.type = 'resource'
        step.context.stash = [
            {
                'address': 'some_address',
                'type': 'resource',
                'values': [
                    'something'
                ]
            }
        ]

        with self.assertRaises(TerraformComplianceInternalFailure):
            it_condition_contain_something(step, 'something')

    @patch('terraform_compliance.steps.steps.seek_key_in_dict', return_value=None)
    def test_it_condition_contain_something_provider_not_found(self, *args):
        step = MockedStep()
        step.context.type = 'provider'
        step.context.stash = []

        self.assertIsNone(it_condition_contain_something(step, 'something'))

    @patch('terraform_compliance.steps.steps.seek_key_in_dict', return_value=True)
    def test_it_condition_contain_something_provider_found(self, *args):
        step = MockedStep()
        step.context.type = 'provider'
        step.context.stash = []

        self.assertTrue(it_condition_contain_something(step, 'something'))

    def test_encryption_is_enabled_not_implemented(self):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'something'
            }
        ]
        with self.assertRaises(TerraformComplianceNotImplemented):
            encryption_is_enabled(step)

    def test_encryption_is_enabled_success(self):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'values': {
                    'storage_encrypted': True
                }
            }
        ]
        self.assertTrue(encryption_is_enabled(step))

    def test_encryption_is_enabled_failure(self):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'address': 'resource'
            }
        ]
        with self.assertRaises(Failure):
            encryption_is_enabled(step)

    def test_it_condition_have_proto_protocol_and_port_port_for_cidr_ports_must_only_fail(self):
        step = MockedStep()
        condition = 'only'
        proto = 'not important'
        port = '1-2'
        cidr = 'not important'
        with self.assertRaises(Failure) as err:
            it_condition_have_proto_protocol_and_port_port_for_cidr(step, condition, proto, port, cidr)

        self.assertEqual(str(err.exception), '"must only" scenario cases must be used either with individual port '
                                             'or multiple ports separated with comma.')

    def test_it_condition_have_proto_protocol_and_port_port_for_cidr_ports_must_only_success(self):
        step = MockedStep()
        step.context.stash = []
        condition = 'not important'
        proto = 'not important'
        port = '1-2'
        cidr = 'not important'
        self.assertTrue(it_condition_have_proto_protocol_and_port_port_for_cidr(step, condition, proto, port, cidr))

    def test_it_condition_have_proto_protocol_and_port_port_for_cidr_ports_with_comma_must_only_success(self):
        step = MockedStep()
        step.context.stash = []
        condition = 'not important'
        proto = 'not important'
        port = '1,2'
        cidr = 'not important'
        self.assertTrue(it_condition_have_proto_protocol_and_port_port_for_cidr(step, condition, proto, port, cidr))

    def test_it_condition_have_proto_protocol_and_port_port_for_cidr_port_success(self):
        step = MockedStep()
        step.context.stash = []
        condition = 'not important'
        proto = 'not important'
        port = '1'
        cidr = 'not important'
        self.assertTrue(it_condition_have_proto_protocol_and_port_port_for_cidr(step, condition, proto, port, cidr))

    def test_i_action_them_count(self):
        step = MockedStep()
        step.context.stash = [1,2,3]
        i_action_them(step, 'count')
        self.assertEqual(step.context.stash, {'values': 3})

    def test_i_action_them_sum(self):
        step = MockedStep()
        with self.assertRaises(TerraformComplianceNotImplemented):
            i_action_them(step, 'something_else')

    def test_i_expect_the_result_is_operator_than_number_more(self):
        step = MockedStep()
        step.context.stash = {'values': 42}
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'more', 41))
        with self.assertRaises(AssertionError) as err:
            i_expect_the_result_is_operator_than_number(step, 'more', 43)
        self.assertEqual(str(err.exception), '42 is not more than 43')

    def test_i_expect_the_result_is_operator_than_number_more_and_equal(self):
        step = MockedStep()
        step.context.stash = {'values': 42}
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'more and equal', 42))
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'more and equal', 41))
        with self.assertRaises(AssertionError) as err:
            i_expect_the_result_is_operator_than_number(step, 'more and equal', 43)
        self.assertEqual(str(err.exception), '42 is not more and equal than 43')

    def test_i_expect_the_result_is_operator_than_number_less(self):
        step = MockedStep()
        step.context.stash = {'values': 42}
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'less', 43))
        with self.assertRaises(AssertionError) as err:
            i_expect_the_result_is_operator_than_number(step, 'less', 41)
        self.assertEqual(str(err.exception), '42 is not less than 41')

    def test_i_expect_the_result_is_operator_than_number_less_and_equal(self):
        step = MockedStep()
        step.context.stash = {'values': 42}
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'less and equal', 43))
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'less and equal', 42))
        with self.assertRaises(AssertionError) as err:
            i_expect_the_result_is_operator_than_number(step, 'less and equal', 41)
        self.assertEqual(str(err.exception), '42 is not less and equal than 41')

    def test_i_expect_the_result_is_more_than_number_failure(self):
        step = MockedStep()
        step.context.stash = dict(values=3)
        with self.assertRaises(TerraformComplianceNotImplemented) as err:
            self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'invalid operator', 1))
        self.assertEqual(str(err.exception), 'Invalid operator: invalid operator')

    def test_it_fails(self):
        step = MockedStep()
        step.context.type = 'some_type'
        step.context.name = 'some_name'
        with self.assertRaises(Failure):
            it_fails(step)