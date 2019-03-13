from unittest import TestCase
from terraform_compliance.main import ReadableDir, cli
from tests.mocks import MockedArgumentParser, MockedArgHandling
from unittest.mock import patch
import os


class TestMain(TestCase):

    def test_readable_dir_call_git_repository_success(self):
        class Namespace(object):
            pass

        resp = ReadableDir('parser', 'value', 'git:value').__call__('parser', Namespace, 'git:value')
        self.assertEqual(Namespace.value, 'value')
        self.assertTrue(resp)


    @patch.object(os.path, 'isdir', return_value=False)
    def test_readable_dir_call_not_a_local_directory(self, *args):
        class Namespace(object):
            pass

        with self.assertRaises(SystemExit):
            ReadableDir('parser', 'value', 'non_existing_dir').__call__('parser', Namespace, 'non_existing_dir')

    @patch.object(os.path, 'isdir', return_value=True)
    @patch.object(os, 'access', return_value=True)
    def test_readable_dir_call_is_a_local_dir(self, *args):
        class Namespace(object):
            pass

        resp = ReadableDir('parser', 'value', 'value').__call__('parser', Namespace, 'value')
        self.assertEqual(Namespace.value, 'value')
        self.assertTrue(resp)

    @patch.object(os.path, 'isdir', return_value=True)
    @patch.object(os, 'access', return_value=False)
    def test_readable_dir_call_can_not_access_dir(self, *args):
        class Namespace(object):
            pass

        with self.assertRaises(SystemExit):
            ReadableDir('parser', 'value', 'non_accessible_dir').__call__('parser', Namespace, 'non_accessible_dir')

    # Unfortunately current cli() structure doesn't allow us to test everything that we want.
    # These tests needs to be refactored when cli() is suitable for tests.

    @patch('terraform_compliance.main.mkdtemp', return_value='/tmp/something')
    @patch('terraform_compliance.main.copy_tree', return_value=True)
    @patch('terraform_compliance.main.rmtree', return_value=True)
    @patch('terraform_compliance.main.Repo', return_value=True)
    @patch('terraform_compliance.main.load_tf_files', return_value=True)
    @patch('terraform_compliance.main.call_radish', return_value=True)
    def test_cli_use_local_dirs_for_all(self, *args):
        self.assertTrue(cli(MockedArgHandling(), MockedArgumentParser('test', 'test description')))

    @patch('terraform_compliance.main.mkdtemp', return_value='/tmp/something')
    @patch('terraform_compliance.main.copy_tree', return_value=True)
    @patch('terraform_compliance.main.rmtree', return_value=True)
    @patch('terraform_compliance.main.Repo', return_value=True)
    @patch('terraform_compliance.main.load_tf_files', return_value=True)
    @patch('terraform_compliance.main.call_radish', return_value=True)
    def test_cli_use_remote_dir_for_features(self, *args):
        args = MockedArgHandling()
        args.ssh_key = False
        args.features = 'git:..'
        self.assertTrue(cli(args, MockedArgumentParser('test', 'test description')))

    @patch('terraform_compliance.main.mkdtemp', return_value='/tmp/something')
    @patch('terraform_compliance.main.copy_tree', return_value=True)
    @patch('terraform_compliance.main.rmtree', return_value=True)
    @patch('terraform_compliance.main.Repo', return_value=True)
    @patch('terraform_compliance.main.load_tf_files', return_value=True)
    @patch('terraform_compliance.main.call_radish', return_value=True)
    def test_cli_use_remote_dir_for_terraform_files(self, *args):
        args = MockedArgHandling()
        args.ssh_key = False
        args.tf_dir = 'git:..'
        self.assertTrue(cli(args, MockedArgumentParser('test', 'test description')))
