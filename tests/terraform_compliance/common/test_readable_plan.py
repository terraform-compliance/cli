from unittest import TestCase
from terraform_compliance.common.readable_plan import ReadablePlan, filetype
from terraform_compliance.common.exceptions import TerraformComplianceInternalFailure

import os
from mock import patch


class TestReadablePlan(TestCase):

    @patch.object(os.path, 'isfile', return_value=False)
    def test_readable_plan_is_not_a_file(self, *args):
        class Namespace(object):
            pass

        with self.assertRaises(SystemExit):
            ReadablePlan('parser', 'value').__call__('parser', Namespace, 'not_a_file')

    @patch.object(os.path, 'isfile', return_value=True)
    @patch.object(filetype, 'guess', return_value='something')
    @patch.object(os.path, 'isfile', return_value=True)
    @patch.object(filetype, 'guess', return_value=None)
    @patch('terraform_compliance.common.readable_plan.convert_terraform_plan_to_json', return_value=None)
    def test_readable_plan_filetype_guess_is_none(self, *args):
        class Namespace(object):
            pass

        with self.assertRaises(TerraformComplianceInternalFailure):
            ReadablePlan('parser', 'value').__call__('parser', Namespace, 'git:value')

    @patch.object(os.path, 'isfile', return_value=True)
    @patch.object(filetype, 'guess', return_value='something')
    @patch('terraform_compliance.common.readable_plan.convert_terraform_plan_to_json', return_value='something')

    def test_readable_plan_convert_terraform_files(self, *args):
        class Namespace(object):
            pass

        with self.assertRaises(TerraformComplianceInternalFailure):
            ReadablePlan('parser', 'value').__call__('parser', Namespace, 'git:value')

    @patch.object(os.path, 'isfile', return_value=True)
    @patch.object(filetype, 'guess', return_value=None)
    def test_readable_plan_filetype_guess_is_none(self, *args):
        class Namespace(object):
            pass

        with self.assertRaises(TerraformComplianceInternalFailure):
            ReadablePlan('parser', 'value').__call__('parser', Namespace, 'git:value')

    @patch.object(os.path, 'isfile', return_value=True)
    @patch.object(filetype, 'guess', return_value=True)
    @patch('terraform_compliance.common.readable_plan.convert_terraform_plan_to_json', return_value='/bin/ls')
    def test_readable_plan_file_is_not_json(self, *args):
        class Namespace(object):
            pass

        with self.assertRaises(SystemExit):
            ReadablePlan('parser', 'value').__call__('parser', Namespace, 'git:value')
