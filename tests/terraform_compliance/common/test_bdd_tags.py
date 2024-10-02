from unittest import TestCase, mock
from terraform_compliance.common.bdd_tags import look_for_bdd_tags
from terraform_compliance.extensions.override_radish_utctime import current_utc_time
from tests.mocks import MockedStep, MockedTags

class TestBddTags(TestCase):

    @mock.patch('radish.extensions.time_recorder.datetime')
    def test_unchanged_step_object(self, mock_datetime):
        mock_datetime.utcnow.side_effect = current_utc_time  # Patches within radish
        step = MockedStep()
        look_for_bdd_tags(step)
        self.assertFalse(step.context.no_failure)
        self.assertIsNone(step.context.failure_class)

    @mock.patch('radish.extensions.time_recorder.datetime')
    def test_warning_case(self, mock_datetime):
        mock_datetime.utcnow.side_effect = current_utc_time  # Patches within radish
        step = MockedStep()
        step.all_tags = [MockedTags(name='warning')]
        look_for_bdd_tags(step)
        self.assertTrue(step.context.no_failure)
        self.assertEqual(step.context.failure_class, 'warning')