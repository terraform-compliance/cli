from unittest import TestCase
from terraform_compliance.steps.steps import (
    i_action_them,
    i_expect_the_result_is_operator_than_number,
    it_condition_contain_something,
    encryption_is_enabled,
    its_value_condition_match_the_search_regex_regex,
    its_value_must_be_set_by_a_variable,
    it_condition_have_proto_protocol_and_port_port_for_cidr
)
from tests.mocks import MockedStep, MockedWorld, MockedTerraformPropertyList, MockedTerraformResourceList, MockedTerraformResource
from mock import patch


class Test_Step_Cases(TestCase):

    def setUp(self):
        self.step = MockedStep()

    def test_i_action_them_count(self):
        step = MockedStep()
        step.context.stash.resource_list = [1,2,3]
        i_action_them(step, 'count')
        self.assertEqual(step.context.stash, 3)

    def test_i_action_them_sum(self):
        step = MockedStep()
        step.context.stash.resource_list = [MockedTerraformResource(), MockedTerraformResource(), MockedTerraformResource()]
        i_action_them(step, 'sum')
        self.assertEqual(step.context.stash, 6)

    def test_i_action_them_undefined(self):
        # with self.assertRaises():
        self.assertIsNone(i_action_them(self.step, 'undefined action'))

    def test_i_action_them_resource_list_as_dict(self):
        step = MockedStep()
        step.context.stash.resource_list = None
        self.assertIsNone(i_action_them(step, 'something that is not important'))

    def test_i_expect_the_result_is_operator_than_number_resource_list_as_dict(self):
        step = MockedStep()
        step.context.stash = 42
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'operator', 'not_important'))

    def test_i_expect_the_result_is_more_than_number_success(self):
        step = MockedStep()
        step.context.stash = 1
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'more', 0))

    def test_i_expect_the_result_is_more_than_number_failure(self):
        step = MockedStep()
        step.context.stash = 1
        with self.assertRaises(AssertionError) as err:
            self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'more', 1))
        self.assertEqual(str(err.exception), '1 is not more than 1')

    def test_i_expect_the_result_is_more_and_equal_than_number_success(self):
        step = MockedStep()
        step.context.stash = 1
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'more and equal', 0))
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'more and equal', 1))

    def test_i_expect_the_result_is_more_and_equal_than_number_failure(self):
        step = MockedStep()
        step.context.stash = 1
        with self.assertRaises(AssertionError) as err:
            i_expect_the_result_is_operator_than_number(step, 'more and equal', 2)
        self.assertEqual(str(err.exception), '1 is not more and equal than 2')

    def test_i_expect_the_result_is_less_than_number_success(self):
        step = MockedStep()
        step.context.stash = 1
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'less', 2))

    def test_i_expect_the_result_is_less_than_number_failure(self):
        step = MockedStep()
        step.context.stash = 1
        with self.assertRaises(AssertionError) as err:
            i_expect_the_result_is_operator_than_number(step, 'less', 1)
        self.assertEqual(str(err.exception), '1 is not less than 1')

    def test_i_expect_the_result_is_less_and_equal_than_number_success(self):
        step = MockedStep()
        step.context.stash = 1
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'less and equal', 1))
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'less and equal', 2))

    def test_i_expect_the_result_is_less_and_equal_than_number_failure(self):
        step = MockedStep()
        step.context.stash = 1
        with self.assertRaises(AssertionError) as err:
            i_expect_the_result_is_operator_than_number(step, 'less and equal', 0)
        self.assertEqual(str(err.exception), '1 is not less and equal than 0')

    def test_i_expect_the_result_is_invalid_operator_than_number_failure(self):
        step = MockedStep()
        step.context.stash = 1
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'invalid_operator', 0))

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

    def test_its_value_must_be_set_by_a_variable_resource_list(self):
        step = MockedStep()
        step.context.stash = MockedTerraformResourceList()
        step.context.search_value = 'something'
        self.assertIsNone(its_value_must_be_set_by_a_variable(step))

    @patch.object(MockedTerraformResourceList, 'property', return_value=MockedTerraformResourceList())
    def test_its_value_must_be_set_by_a_variable(self, *args):
        step = MockedStep()
        step.context.stash = MockedTerraformResourceList()
        step.context.search_value = MockedTerraformResourceList()
        self.assertIsNone(its_value_must_be_set_by_a_variable(step))
