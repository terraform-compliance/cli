from unittest import TestCase
from terraform_compliance.main import ReadableDir, cli
from tests.mocks import MockedArgumentParser, MockedArgHandling
from unittest.mock import patch
import os


class TestMain(TestCase):

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
