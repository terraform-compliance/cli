from unittest import TestCase
from terraform_compliance.common.readable_dir import ReadableDir
import os
from mock import patch


class TestReadableDir(TestCase):
    def test_readable_dir_call_git_repository_success(self):
        class Namespace(object):
            pass

        resp = ReadableDir('parser', 'value').__call__('parser', Namespace, 'git:value')
        self.assertEqual(Namespace.value, 'value')
        self.assertTrue(resp)


    @patch.object(os.path, 'isdir', return_value=False)
    def test_readable_dir_call_not_a_local_directory(self, *args):
        class Namespace(object):
            pass

        with self.assertRaises(SystemExit):
            ReadableDir('parser', 'value').__call__('parser', Namespace, 'non_existing_dir')

    @patch.object(os.path, 'isdir', return_value=True)
    @patch.object(os, 'access', return_value=True)
    def test_readable_dir_call_is_a_local_dir(self, *args):
        class Namespace(object):
            pass

        resp = ReadableDir('parser', 'value').__call__('parser', Namespace, 'value')
        self.assertEqual(Namespace.value, 'value')
        self.assertTrue(resp)

    @patch.object(os.path, 'isdir', return_value=True)
    @patch.object(os, 'access', return_value=False)
    def test_readable_dir_call_can_not_access_dir(self, *args):
        class Namespace(object):
            pass

        with self.assertRaises(SystemExit):
            ReadableDir('parser', 'value').__call__('parser', Namespace, 'non_accessible_dir')

