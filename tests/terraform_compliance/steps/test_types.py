from unittest import TestCase
from terraform_compliance.steps.steps import custom_type_any, custom_type_section


class Test_Steps_Custom_Type(TestCase):

    def test_custom_type_any(self):
        self.assertEqual(custom_type_any('AnyType'), 'AnyType')
        self.assertEqual(custom_type_any('13/135lx.13-_f19  39'), '13/135lx.13-_f19  39')

    def test_custom_type_section(self):
        for section in ['resource', 'provider', 'data', 'module', 'output', 'terraform', 'variable']:
            self.assertEqual(custom_type_section(section), section)

        self.assertIsNone(custom_type_section('this is something else'))