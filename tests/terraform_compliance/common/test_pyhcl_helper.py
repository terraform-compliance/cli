from unittest import TestCase
from terraform_compliance.common.pyhcl_helper import (
    load_tf_files,
    pad_invalid_tf_files,
    pad_tf_file,
    parse_hcl_value
)
from tests.mocks import MockedValidator
from os import remove, path, environ
from unittest.mock import patch


class TestPyHCLHelper(TestCase):

    def test_pad_tf_file(self):
        tmpFile = '.terraform_compliance_unit_tests.tf'
        pad_tf_file(tmpFile)
        with open(tmpFile, 'r') as file:
            contents = file.read()
            remove(tmpFile)
            self.assertEqual(contents, '\n\nvariable {}')

    @patch('terraform_compliance.common.pyhcl_helper.pad_tf_file', return_value=None)
    def test_pad_invalid_tf_files(self, *args):
        self.assertTrue(pad_invalid_tf_files('filename\nUnexpected end of file'))
        self.assertFalse(pad_invalid_tf_files('filename\nAnother message'))

    @patch.object(path, 'isdir', return_value=True)
    def test_load_tf_files_exit_for_dot_terraform(self, *args):
        with self.assertRaises(SystemExit):
            load_tf_files('a_directory')

    @patch.object(path, 'isdir', return_value=False)
    @patch('terraform_compliance.common.pyhcl_helper.Validator', side_effect=MockedValidator)
    def test_load_tf_files_valueerror(self, *args):
        with self.assertRaises(SystemExit):
            load_tf_files('valueerror')

    @patch.object(path, 'isdir', return_value=False)
    @patch('terraform_compliance.common.pyhcl_helper.Validator', side_effect=MockedValidator)
    @patch('terraform_compliance.common.pyhcl_helper.pad_invalid_tf_files', return_value=None)
    def test_load_tf_files_terraformsyntaxexception(self, *args):
        self.assertTrue(load_tf_files('syntaxexception'))
        self.assertEqual(environ['MockedValidator.state'], '1')
        del environ['MockedValidator.state']

    @patch.object(path, 'isdir', return_value=False)
    @patch('terraform_compliance.common.pyhcl_helper.Validator', side_effect=MockedValidator)
    @patch('terraform_compliance.common.pyhcl_helper.pad_invalid_tf_files', return_value=None)
    def test_load_tf_files_success(self, *args):
        self.assertTrue(load_tf_files('passed'))
        self.assertTrue(environ.get('MockedValidator.state', None) is None)


    def test_parse_hcl_value_return_same(self):
        tf_conf = dict(variable=dict(key='value'))
        self.assertEqual(parse_hcl_value('some_string', tf_conf), 'some_string')
