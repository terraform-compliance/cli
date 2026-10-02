from unittest import TestCase
from terraform_compliance.common import readable_plan
from terraform_compliance.common.readable_plan import ReadablePlan, filetype
from terraform_compliance.common.exceptions import TerraformComplianceInternalFailure

import os
import tempfile
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

    def test_readable_plan_json_backend_honours_parse_float(self):
        # The json backend used to read the plan must accept parse_float=str so
        # version strings such as "1.30" are preserved instead of collapsing to
        # 1.3 (#799, fixing #752). orjson, which this module used to import as
        # json, rejects the keyword with "orjson.loads() takes no keyword
        # arguments", which broke plan loading entirely.
        data = readable_plan.json.loads('{"version": 1.30}', parse_float=str)
        self.assertEqual(data['version'], '1.30')

    @patch.object(filetype, 'guess', return_value=None)
    def test_readable_plan_loads_plan_with_numeric_version(self, *args):
        # A valid plan that carries an unquoted numeric version must load without
        # raising. Before the fix this raised a TypeError from orjson that the
        # broad except reported as "Invalid file type.".
        class Namespace(object):
            pass

        plan = (
            '{"format_version": "1.0", "terraform_version": "1.5.0", '
            '"planned_values": {"root_module": {}}, '
            '"configuration": {"provider_config": {"aws": {}}}, '
            '"module_version": 1.30}'
        )

        descriptor, plan_path = tempfile.mkstemp(suffix='.json')
        os.close(descriptor)
        with open(plan_path, 'w', encoding='utf-8') as plan_file:
            plan_file.write(plan)

        try:
            result = ReadablePlan('parser', 'value').__call__('parser', Namespace, plan_path)
            self.assertTrue(result)
            self.assertEqual(Namespace.value, os.path.abspath(plan_path))
        finally:
            os.remove(plan_path)
