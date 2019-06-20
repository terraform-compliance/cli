import sys
import os
from argparse import Action


class ReadableDir(Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(ReadableDir, self).__init__(option_strings, dest, **kwargs)
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
