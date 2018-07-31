import sys
import os
from argparse import ArgumentParser, Action
from terraform_compliance import Validator
from radish.main import main as call_radish
from tempfile import mkdtemp
from shutil import rmtree
from git import Repo

__app_name__ = "terraform-compliance"
__version__ = "0.2.0"


class ArgHandling(object):
    pass

#TODO: Handle all directory/protocol handling via a better class structure here.
#TODO: Extend git: (on features or tf files argument) into native URLs instead of using a prefix here.

class readable_dir(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values

        # Check if the given directory is actually a git repo
        if prospective_dir.startswith('git:'):
            print('Using remote git repository: {}'.format(prospective_dir[4:]))
            setattr(namespace, self.dest, prospective_dir[4:])
            return True

        # Check if the given path is a directory really
        if not os.path.isdir(prospective_dir):
            print('ERROR: {} is not a directory.'.format(prospective_dir))
            sys.exit(1)

        # Check if we have access to that directory
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, prospective_dir)
            return True

        print('ERROR: Can not read {}'.format(prospective_dir))
        sys.exit(1)


def cli():
    print('{} v{} initiated'.format(__app_name__, __version__))

    argument = ArgHandling()
    parser = ArgumentParser(prog=__app_name__,
                            description="BDD Test Framework for Hashicorp terraform")
    parser.add_argument("--features", "-f", dest="features", metavar='feature_directory', action=readable_dir,
                        help="Directory consists of BDD features", required=True)
    parser.add_argument("--tfdir", "-t", dest="tf_dir", metavar='terraform_directory', action=readable_dir,
                        help="Directory (or git repository with 'git:' prefix) consists of Terraform Files", required=True)

    _, radish_arguments = parser.parse_known_args(namespace=argument)

    steps_directory = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'steps')
    print('Steps    : {}'.format(steps_directory))

    if argument.features.startswith('http'):
        features_git_repo = argument.features
        argument.features = mkdtemp()
        Repo.clone_from(features_git_repo, argument.features)
    features_directory = os.path.join(os.path.abspath(argument.features))
    print('Features : {}{}'.format(features_directory, (' ({})'.format(features_git_repo) if 'features_git_repo' in locals() else '')))

    if argument.tf_dir.startswith('http'):
        tf_git_repo = argument.tf_dir
        argument.tf_dir = mkdtemp()
        Repo.clone_from(tf_git_repo, argument.tf_dir)
    tf_directory = os.path.join(os.path.abspath(argument.tf_dir))
    print('TF Files : {}{}'.format(tf_directory, (' ({})'.format(tf_git_repo) if 'tf_git_repo' in locals() else '')))

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


#TODO: Implement a cleanup for temporary directories since they are not deleted.
