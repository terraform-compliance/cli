import sys
import os
from argparse import Action
import filetype
from terraform_compliance.common.terraform_files import convert_terraform_plan_to_json
from terraform_compliance.common.exceptions import TerraformComplianceInternalFailure

try:
    import orjson as json
except ImportError:
    import json


class ReadablePlan(Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(ReadablePlan, self).__init__(option_strings, dest, **kwargs)
        self.option_strings = option_strings
        self.dest = dest
        self.nargs = kwargs.get('nargs', None)
        self.const = kwargs.get('const', None)
        self.default = kwargs.get('default', None)
        self.type = kwargs.get('type', None)
        self.choices = kwargs.get('choices', None)
        self.required = kwargs.get('required', None)
        self.help = kwargs.get('help', None)
        self.metavar = kwargs.get('metavar', None)
        self.parser = kwargs.get('parser', None)

    def __call__(self, parser, namespace, values, option_string=None):
        # Check if the given path is a file
        if not os.path.isfile(values):
            print('ERROR: {} is not a file.'.format(values))
            sys.exit(1)

        # Check if the given file is a native terraform plan file
        given_file = filetype.guess(values)

        if given_file is not None:
            terraform_executable = getattr(namespace, 'terraform_file', None)
            values = convert_terraform_plan_to_json(os.path.abspath(values), terraform_executable)

        # Check if the given file is a json file.
        try:
            plan_lines = [line for line in open(values, 'r', encoding='utf-8')]

            # Some Github Actions (hashicorp/setup-terraform) has internal wrappers which is
            # breaking the json file that is read by the terraform-compliance
            file_change_required = False
            if len(plan_lines) > 1:
                plan_lines = plan_lines[1]
                file_change_required = True
            else:
                plan_lines = plan_lines[0]

            data = json.loads(plan_lines)

            # Write the changed plan file to the same file, since it is used in other places.
            if file_change_required:
                with open(values, 'w', encoding='utf-8') as plan_file:
                    plan_file.write(plan_lines)

        except json.JSONDecodeError:
            print('ERROR: {} is not a valid JSON file'.format(values))
            sys.exit(1)
        except UnicodeDecodeError:
            print('ERROR: {} is not a valid JSON file.'.format(values))
            print('       Did you try to convert the binary plan file to json with '
                  '"terraform show -json {} > {}.json" ?'.format(values, values))
            sys.exit(1)
        except:
            raise TerraformComplianceInternalFailure('Invalid file type.')

        # Check if this is a correct terraform plan file
        try:
            assert data['format_version']
            assert data['terraform_version']

            # Check if this is a state file
            if 'values' in data:
                assert data['values']['root_module'].get('resources', data['values']['root_module'].get('child_modules'))

            # Then it must be a terraform plan file
            else:
                assert data['planned_values']
                assert data['configuration']

        except KeyError:
            print('ERROR: {} is not a valid terraform plan json output.'.format(values))
            sys.exit(1)

        setattr(namespace, self.dest, os.path.abspath(values))
        return True
