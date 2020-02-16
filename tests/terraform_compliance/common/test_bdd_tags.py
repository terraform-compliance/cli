from unittest import TestCase
from terraform_compliance.common.bdd_tags import look_for_bdd_tags
from terraform_compliance.common.exceptions import Failure
from tests.mocks import MockedStep, MockedTags


class TestBddTags(TestCase):

    def test_unchanged_step_object(self):
        step = MockedStep()
        look_for_bdd_tags(step)
        self.assertFalse(step.context.no_failure)
        self.assertIsNone(step.context.failure_class)

    def test_warning_case(self):
        step = MockedStep()
        step.all_tags = [MockedTags(name='warning')]
        look_for_bdd_tags(step)
        self.assertTrue(step.context.no_failure)
        self.assertEqual(step.context.failure_class, 'warning')
