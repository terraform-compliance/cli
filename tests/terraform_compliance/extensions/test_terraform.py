from unittest import TestCase
from terraform_compliance.extensions.terraform import TerraformParser
from tests.mocks import MockedData
from mock import patch

class TestTerraformParser(TestCase):

    @patch.object(TerraformParser, '_read_file', return_value=MockedData.mocked_plan_outputs['security_group_mounting'])
    def test_security_group_mounting_success(self, *args):
            obj = TerraformParser('somefile')
            self.assertTrue('ingress' in obj.resources['aws_security_group.example']['values'])
