import os
from argparse import ArgumentParser
from radish.main import main as call_radish
from tempfile import mkdtemp
from git import Repo
from terraform_compliance.common.pyhcl_helper import load_tf_files
from distutils.dir_util import copy_tree
from shutil import rmtree
from terraform_compliance.common.readable_dir import ReadableDir


__app_name__ = "terraform-compliance"
__version__ = "0.3.9"


class ArgHandling(object):
    pass

#TODO: Handle all directory/protocol handling via a better class structure here.
#TODO: Extend git: (on features or tf files argument) into native URLs instead of using a prefix here.

def cli():
    args = ArgHandling()
    parser = ArgumentParser(prog=__app_name__,
                            description="BDD Test Framework for Hashicorp terraform")
    parser.add_argument("--features", "-f", dest="features", metavar='feature_directory', action=ReadableDir,
                        help="Directory consists of BDD features", required=True)
    parser.add_argument("--tfdir", "-t", dest="tf_dir", metavar='terraform_directory', action=ReadableDir,
                        help="Directory (or git repository with 'git:' prefix) consists of Terraform Files",
                        required=True)
    parser.add_argument("--version", "-v", action="version", version=__version__)

    _, radish_arguments = parser.parse_known_args(namespace=args)

    print('{} v{} initiated'.format(__app_name__, __version__))

    steps_directory = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'steps')
    print('Steps    : {}'.format(steps_directory))

    # A remote repository used here
    if args.features.startswith('http'):
        features_git_repo = args.features
        args.features = mkdtemp()
        Repo.clone_from(features_git_repo, args.features)
    features_directory = os.path.join(os.path.abspath(args.features))
    print('Features : {}{}'.format(features_directory, (' ({})'.format(features_git_repo) if 'features_git_repo' in locals() else '')))

    tf_tmp_dir = mkdtemp()

    # A remote repository is used here.
    if args.tf_dir.startswith('http'):
        tf_git_repo = args.tf_dir
        Repo.clone_from(tf_git_repo, tf_tmp_dir)

    # A local directory is used here
    else:
        # Copy the given local directory to another place, since we may change some tf files for compatibility.
        copy_tree(args.tf_dir, tf_tmp_dir)

    tf_directory = os.path.join(os.path.abspath(tf_tmp_dir))
    print('TF Files : {} ({})'.format(tf_directory, args.tf_dir))

    commands = ['radish',
                '--write-steps-once',
                features_directory,
                '--basedir', steps_directory,
                '--user-data=tf_dir={}'.format(tf_directory)]
    commands.extend(radish_arguments)

    load_tf_files(tf_directory)
    print('Running tests.')
    result = call_radish(args=commands[1:])

    # Delete temporary directory we created
    print('Cleaning up.')
    rmtree(tf_directory)


if __name__ == '__main__':
    cli()
