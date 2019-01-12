from sys import exc_info, exit
from os.path import isdir
from terraform_compliance import Validator
from terraform_validate.terraform_validate import TerraformSyntaxException
from terraform_compliance.common.exceptions import TerraformComplianceInvalidConfig
from terraform_compliance.common.helper import expand_variable
from shutil import rmtree
from hcl import loads


def load_tf_files(tf_directory):
    result = False
    print('Reading terraform files.')

    if isdir('{}/.terraform'.format(tf_directory)):
        rmtree('{}/.terraform'.format(tf_directory))

    while result is False:
        try:
            Validator(tf_directory)
            print('All HCL files look good.')
            return True

        except ValueError:
            print('Unable to validate Terraform Files.')
            print('ERROR: {}'.format(exc_info()[1]))
            exit(1)

        except TerraformSyntaxException:
            result = pad_invalid_tf_files(exc_info()[1]) is True

        except TerraformComplianceInvalidConfig:
            pass

    return result


def pad_invalid_tf_files(exception_message):
    exception_message = str(exception_message).split('\n')
    if 'Unexpected end of file' in exception_message[1]:
        filename = exception_message[0].split(' ')[-1:][0]
        print('Invalid HCL file: {}. Fixing it.'.format(filename))
        pad_tf_file(filename)
        return True
    elif 'Invalid terraform configuration in ' in exception_message[0]:
        raise TerraformComplianceInvalidConfig('ERROR: Invalid terraform configuration {}'.format(exception_message[1]))

    return False


def pad_tf_file(file):
    with open(file, 'a') as f:
        f.write('\n\nvariable {}')


def parse_hcl_value(hcl_string, tf_config):
    if str(hcl_string).startswith(('${', '"${')):
        hcl = "key = \"{}\"".format(str(hcl_string).replace("'", "\"").lower())

        try:
            hcl = loads(hcl)
            if "." in hcl['key']:
                hcl['key'] = expand_variable(tf_conf=tf_config, value=hcl['key'])
            return eval(hcl['key'].replace('${', '{'))
        except ValueError:
            return hcl_string

    if type(hcl_string) is dict:
        hcl_string = {k.lower(): v for k, v in hcl_string.items()}

    return hcl_string
