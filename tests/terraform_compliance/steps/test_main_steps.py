from unittest import TestCase
from terraform_compliance.steps.steps import (
    i_action_them,
    i_expect_the_result_is_operator_than_number,
    it_condition_contain_something,
    encryption_is_enabled,
    its_value_condition_match_the_search_regex_regex,
    its_value_must_be_set_by_a_variable,
    it_must_not_have_proto_protocol_and_port_port_for_cidr
)
from tests.mocks import MockedStep, MockedWorld


class Test_Step_Cases(TestCase):

    def setUp(self):
        self.step = MockedStep()
        self.radish_world = MockedWorld()

    def test_i_action_them_count(self):
        step = MockedStep()
        step.context.stash.resource_list = [1,2,3]
        i_action_them(step, 'count')
        self.assertEqual(step.context.stash, 3)

    def test_i_action_them_sum(self):
        step = MockedStep()
        step.context.stash.resource_list = [1,2,3]
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
        step.context.stash.resource_list = None
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
        self.assertIsNone(it_condition_contain_something(step, 'condition', 'not_important'))

    def test_it_condition_contain_something_property_can_not_be_found(self):
        pass

    def test_it_condition_must_something_property_can_not_be_found(self):
        pass

    def test_it_condition_must_something_property_is_found(self):
        pass

    def test_it_condition_should_something_property_is_found(self):
        pass
