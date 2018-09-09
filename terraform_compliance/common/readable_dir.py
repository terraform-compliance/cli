import sys
import os
from argparse import Action


class ReadableDir(Action):
    def __init__(self, dest, required, help, option_strings=None, metavar=None):
        super(ReadableDir, self).__init__(dest, required, help, option_strings, metavar)
        self.dest = dest
        self.required = required
        self.help = help
        self.option_strings = option_strings
        self.metavar = metavar

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