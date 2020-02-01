from unittest import TestCase
from terraform_compliance.extensions.ext_radish_bdd import skip_step, step_condition
from tests.mocks import MockedStep, MockedWorld
from mock import patch


class TestRadishBddExtension(TestCase):
    def test_step_condition(self):
        step = MockedStep()

        step.sentence = 'Given I do this'
        self.assertEqual(step_condition(step), 'given')

        step.sentence = 'When I do this'
        self.assertEqual(step_condition(step), 'when')

        step.sentence = 'Then I do this'
        self.assertEqual(step_condition(step), 'then')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_skip_step(self, *args):
        step = MockedStep()
        skip_step(step)
        self.assertEqual(step.state, 'skipped')