from unittest import TestCase
from terraform_compliance.steps.steps import i_have_name_section_configured, i_have_resource_defined
from tests.mocks import MockedStep, MockedWorld, MockedWorldConfigTerraform


class TestGivenStepCases(TestCase):

    def setUp(self):
        self.step = MockedStep()
        self.radish_world = MockedWorld()

    def test_i_have_name_section_configured(self):
        i_have_name_section_configured(self.step, 'resource_type', 'resource', self.radish_world)
        self.assertEqual(self.step.context.stash.resource_list[0], MockedWorldConfigTerraform().terraform_config['resource']['resource_type'])

        i_have_name_section_configured(self.step, 'aws', 'provider', self.radish_world)
        self.assertEqual(self.step.context.stash, MockedWorldConfigTerraform().terraform_config['provider']['aws'])

        i_have_name_section_configured(self.step, 'non_existent', 'something_else', self.radish_world)
        self.assertEqual(self.step.context.stash, MockedWorldConfigTerraform().terraform_config['something_else'])

        i_have_name_section_configured(self.step, 'AWS S3 Bucket', 'resource', self.radish_world)
        self.assertEqual(self.step.context.stash.resource_list[0], MockedWorldConfigTerraform().terraform_config['resource']['aws_s3_bucket'])

    def test_i_have_resource_defined(self):
        i_have_resource_defined(self.step, 'resource_type', self.radish_world)
        self.assertEqual(self.step.context.stash.resource_list[0], MockedWorldConfigTerraform().terraform_config['resource']['resource_type'])

        i_have_resource_defined(self.step, 'AWS S3 Bucket', self.radish_world)
        self.assertEqual(self.step.context.stash.resource_list[0], MockedWorldConfigTerraform().terraform_config['resource']['aws_s3_bucket'])

