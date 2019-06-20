from unittest import TestCase
from terraform_compliance.common.pip_helper import subprocess, reinstall_radish
from mock import patch


class TestPipHelper(TestCase):

    @patch.object(subprocess, 'call', return_value=None)
    def test_reinstall_radish(self, *args):
        with self.assertRaises(SystemExit) as context:
            reinstall_radish()
