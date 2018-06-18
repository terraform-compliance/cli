import sys
import os
from argparse import ArgumentParser, ArgumentTypeError, Action
from terraform_compliance import Validator
from radish.main import main as call_radish

__app_name__ = "terraform-compliance"
__version__ = "0.1.0"


class ArgHandling(object):
    def __init__(self):
        self.features = None
        self.steps = None
        self.tf_dir = None

class readable_dir(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            print('Invalid use or arguments: {}'.format(prospective_dir))
            sys.exit(1)

        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            print('Invalid use or arguments: {}'.format(prospective_dir))
            sys.exit(1)


def cli():
    argument = ArgHandling()
    parser = ArgumentParser(prog=__app_name__,
                            description="BDD Test Framework for Hashicorp terraform")
    try:
        parser.add_argument("--features", "-f", dest="features", metavar='feature_directory', action=readable_dir,
                        help="Directory consists of BDD features", required=True)
        parser.add_argument("--tfdir", "-t", dest="tf_dir", metavar='terraform_directory', action=readable_dir,
                        help="Directory consists of Terraform Files", required=True)
    except argparse.ArgumentTypeError:
        print('Invalid use or arguments: {}'.format(sys.exc_info()[1]))
        sys.exit(1)

    # parser.parse_args(namespace=argument)
    _, radish_arguments = parser.parse_known_args(namespace=argument)

    print('{} v{} initiated'.format(__app_name__, __version__))

    features_directory = os.path.join(os.path.abspath(argument.features))
    steps_directory = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'steps')
    tf_directory = os.path.join(os.path.abspath(argument.tf_dir))

    print('Features : {}'.format(features_directory))
    print('Steps    : {}'.format(steps_directory))
    print('TF Files : {}'.format(tf_directory))

    commands = ['radish',
                features_directory,
                '--basedir', steps_directory,
                '--user-data=tf_dir={}'.format(tf_directory)]
    commands.extend(radish_arguments)

    try:
        print('Validating terraform files.')
        Validator(tf_directory)
        print('All HCL files look good.')

    except ValueError:
        print('Unable to validate Terraform Files.')
        print('ERROR: {}'.format(sys.exc_info()[1]))
        sys.exit(1)

    print('Running tests.')
    return call_radish(args=commands[1:])
