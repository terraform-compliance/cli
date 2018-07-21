from unittest import TestCase
from terraform_compliance.main import readable_dir
from mock import patch
import os


class TestMain(TestCase):

    def test_readable_dir_call_git_repository_success(self):
        class Namespace(object):
            pass

        resp = readable_dir('parser', 'value', 'git:value').__call__('parser', Namespace, 'git:value')
        self.assertEqual(Namespace.value, 'value')
        self.assertTrue(resp)


    @patch.object(os.path, 'isdir', return_value=False)
    def test_readable_dir_call_not_a_local_directory(self, *args):
        class Namespace(object):
            pass

        with self.assertRaises(SystemExit):
            readable_dir('parser','value','non_existing_dir').__call__('parser', Namespace, 'non_existing_dir')

    @patch.object(os.path, 'isdir', return_value=True)
    @patch.object(os, 'access', return_value=True)
    def test_readable_dir_call_is_a_local_dir(self, *args):
        class Namespace(object):
            pass

        resp = readable_dir('parser', 'value', 'value').__call__('parser', Namespace, 'value')
        self.assertEqual(Namespace.value, 'value')
        self.assertTrue(resp)

    @patch.object(os.path, 'isdir', return_value=True)
    @patch.object(os, 'access', return_value=False)
    def test_readable_dir_call_can_not_access_dir(self, *args):
        class Namespace(object):
            pass

        with self.assertRaises(SystemExit):
            readable_dir('parser','value','non_accessible_dir').__call__('parser', Namespace, 'non_accessible_dir')


    ''' 
    def test_cli_use_local_dirs_for_all(self):
        self.assertTrue(False)

    def test_cli_use_remote_dir_for_features(self):
        self.assertTrue(False)

    def test_cli_use_remote_dir_for_terraform_files(self):
        self.assertTrue(False)

    def test_cli_parse_radish_arguments(self):
        self.assertTrue(False)

    def test_cli_invalid_terraform_files(self):
        self.assertTrue(False)
    '''