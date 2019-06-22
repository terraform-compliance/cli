from unittest import TestCase
from terraform_compliance.common.terraform_files import which, convert_terraform_plan_to_json

import os
from mock import patch


class TestTerraformFiles(TestCase):

    def test_which_success(self):
        self.assertEqual('/bin/ls', which('/bin/ls'))

    def test_which_failure(self):
        self.assertIsNone(which('/something/that/doesnt/exist/hopefully'))

    @patch('terraform_compliance.common.terraform_files.which', return_value=None)
    def test_convert_terraform_plan_to_json(self, *args):
        with self.assertRaises(SystemExit):
            convert_terraform_plan_to_json('some_file')
