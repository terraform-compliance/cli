from unittest import TestCase
from terraform_compliance.steps.steps import (
    i_action_them,
    i_expect_the_result_is_operator_than_number,
    it_condition_contain_something,
    encryption_is_enabled,
    its_value_condition_match_the_search_regex_regex,
    it_condition_have_proto_protocol_and_port_port_for_cidr
)
from terraform_compliance.common.exceptions import TerraformComplianceNotImplemented
from tests.mocks import MockedStep, MockedWorld, MockedTerraformPropertyList, MockedTerraformResourceList, MockedTerraformResource
from mock import patch


class Test_Step_Cases(TestCase):

    def setUp(self):
        self.step = MockedStep()

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
        step.context.stash = dict()
        with self.assertRaises(TerraformComplianceNotImplemented) as err:
            self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'invalid operator', 1))
        self.assertEqual(str(err.exception), 'Invalid operator: invalid operator')

    def test_it_condition_contain_something_resource_list(self):
        step = MockedStep()
        step.context.stash.resource_list = None
        self.assertIsNone(it_condition_contain_something(step, 'should', 'not_important'))

    @patch('terraform_compliance.steps.steps.world', side_effect=MockedWorld())
    def test_it_must_contain_something_property_can_not_be_found(self, *args):
        step = MockedStep()
        step.context.stash = MockedTerraformPropertyList()
        step.sentence = 'Then it must contain'
        with self.assertRaises(AssertionError) as err:
            it_condition_contain_something(step, 'non_existent_property_value', MockedTerraformPropertyList)
        self.assertEqual(str(err.exception), 'non_existent_property_value property in test_name can not be found in ' 
                                             'test_resource_name (test_resource_type). It is set to test_value instead')

    def test_it_condition_must_something_property_can_not_be_found(self):
        step = MockedStep()
        step.context.stash = MockedTerraformResourceList()
        step.sentence = 'Then it must ..'
        with self.assertRaises(Exception) as err:
            it_condition_contain_something(step_obj=step, something=None, resourcelist=MockedTerraformResourceList)
        self.assertEqual(str(err.exception), 'should_have_properties hit')

        step.sentence = 'When it contains'
        it_condition_contain_something(step_obj=step, something=None, resourcelist=MockedTerraformResourceList)
        self.assertEqual(step.state, 'skipped')

    def test_it_condition_must_something_property_is_found(self):
        step = MockedStep()
        step.context.stash = MockedTerraformResourceList()
        step.sentence = 'Then it must ..'
        it_condition_contain_something(step_obj=step, something='something', resourcelist=MockedTerraformResourceList)
        self.assertEqual(step.context.stash[0].__class__, MockedTerraformPropertyList)

    def test_it_condition_must_something_property_stash_is_dict_found(self):
        step = MockedStep()
        step.context.stash = {'something': 'something else'}
        self.assertIsNone(it_condition_contain_something(step_obj=step, something='something', resourcelist=MockedTerraformResourceList))

    def test_it_condition_should_something_property_stash_is_dict_found(self):
        step = MockedStep()
        step.context.stash = {}
        step.sentence = 'Then it must contain'
        with self.assertRaises(AssertionError) as err:
            it_condition_contain_something(step_obj=step, something='something', resourcelist=MockedTerraformResourceList)
        self.assertEqual(str(err.exception), 'something does not exist.')

        step.sentence = 'When it contains'
        step.context.stash = {}
        it_condition_contain_something(step_obj=step, something='something', resourcelist=MockedTerraformResourceList)
        self.assertEqual(step.state, 'skipped')

    def test_encryption_is_enabled_resource_list(self):
        step = MockedStep()
        step.context.stash = MockedTerraformResourceList()
        self.assertIsNone(encryption_is_enabled(step))

    def test_its_value_condition_match_the_search_regex_regex_resource_list(self):
        step = MockedStep()
        step.context.stash = MockedTerraformPropertyList()
        self.assertIsNone(its_value_condition_match_the_search_regex_regex(step, 'condition', 'some_regex'))

    def test_its_value_must_match_the_search_regex_regex_string_unicode_success(self):
        step = MockedStep()
        step.context.stash = 'some string'
        self.assertIsNone(its_value_condition_match_the_search_regex_regex(step, 'must', '^[sometring\s]+$'))

    def test_its_value_must_match_the_search_regex_regex_string_unicode_failure(self):
        step = MockedStep()
        step.context.stash = 'some string'
        step.context.name = 'test name'
        step.context.type = 'test type'
        with self.assertRaises(AssertionError) as err:
            its_value_condition_match_the_search_regex_regex(step, 'must', 'non_match_regex')
        self.assertEqual(str(err.exception), '{} {} tests failed on {} regex: {}'.format(step.context.name,
                                                                                         step.context.type,
                                                                                         'non_match_regex',
                                                                                         step.context.stash))

    def test_its_value_must_match_not_the_search_regex_regex_string_unicode_success(self):
        step = MockedStep()
        step.context.stash = 'some string'
        self.assertIsNone(its_value_condition_match_the_search_regex_regex(step, 'must not', 'non_match_regex'))

    def test_its_value_must_not_match_the_search_regex_regex_string_unicode_failure(self):
        step = MockedStep()
        step.context.stash = 'some string'
        step.context.name = 'test name'
        step.context.type = 'test type'
        with self.assertRaises(AssertionError) as err:
            its_value_condition_match_the_search_regex_regex(step, 'must not', '^[sometring\s]+$')
        self.assertEqual(str(err.exception), '{} {} tests failed on {} regex: {}'.format(step.context.name,
                                                                                         step.context.type,
                                                                                         '^[sometring\s]+$',
                                                                                         step.context.stash))

    def test_its_value_must_match_the_search_regex_regex_success(self):
        step = MockedStep()
        step.context.stash = MockedTerraformPropertyList()
        self.assertIsNone(its_value_condition_match_the_search_regex_regex(step, 'must', '^[tesvalu_\s]+$'))

    def test_its_value_must_match_the_search_regex_regex_failure(self):
        step = MockedStep()
        step.context.stash = MockedTerraformPropertyList()
        with self.assertRaises(AssertionError):
            its_value_condition_match_the_search_regex_regex(step, 'must', 'non_match_regex')

    def test_its_value_must_not_match_the_search_regex_regex_success(self):
        step = MockedStep()
        step.context.stash = MockedTerraformPropertyList()
        self.assertIsNone(its_value_condition_match_the_search_regex_regex(step, 'must not', '^[tesvalu_\s]+$'))

    def test_its_value_must_not_match_the_search_regex_regex_failure(self):
        step = MockedStep()
        step.context.stash = MockedTerraformPropertyList()
        with self.assertRaises(AssertionError):
            its_value_condition_match_the_search_regex_regex(step, 'must not', 'non_match_regex')

