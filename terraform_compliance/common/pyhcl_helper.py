from sys import exc_info, exit
from os.path import isdir
from terraform_compliance import Validator
from terraform_validate.terraform_validate import TerraformSyntaxException
from shutil import rmtree


def load_tf_files(tf_directory):
    result = False
    print('Reading terraform files.')

    if isdir('{}/.terraform'.format(tf_directory)):
        rmtree('{}/.terraform'.format(tf_directory))

    while result is False:
        try:
            Validator(tf_directory)
            print('All HCL files look good.')
            result = True

        except ValueError:
            print('Unable to validate Terraform Files.')
            print('ERROR: {}'.format(exc_info()[1]))
            exit(1)
        except TerraformSyntaxException:
            pad_invalid_tf_files(exc_info()[1])

    return result


def pad_invalid_tf_files(exception_message):
    exception_message = str(exception_message).split('\n')
    if 'Unexpected end of file' in exception_message[1]:
        filename = exception_message[0].split(' ')[-1:][0]
        print('Invalid HCL file: {}. Fixing it.'.format(filename))
        pad_tf_file(filename)
        return True

    return False


def pad_tf_file(file):
    with open(file, 'a') as f:
        f.write('variable {}')
