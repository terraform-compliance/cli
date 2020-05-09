from __future__ import unicode_literals

import colorful
import sys
from radish.exceptions import (
    RadishError,
    HookError,
)
from radish.utils import Failure, console_write
from terraform_compliance.common.defaults import Defaults

from radish.exceptions import (
    LanguageNotSupportedError,
    FeatureFileNotFoundError,
    FeatureFileSyntaxError,
    StepDefinitionNotFoundError,
    StepPatternError,
    StepRegexError,
    SameStepError,
    ScenarioNotFoundError,
)


def write_error(text):
    """
        Writes the given text to the console
    """
    console_write("{} {}: {}".format(Defaults().warning_icon,
                                     Defaults().failure_colour("ERROR"),
                                     Defaults().warning_colour(text)))


def write_failure(failure):
    """
        Writes the failure to the console
    """
    console_write("\n{0}".format(Defaults().failure_colour(failure.traceback)))


def abort(return_code):
    """
        Aborts the program with the given return_code
    """
    sys.exit(return_code)


def handle_exception(exception):
    """
        Handle the given exception

        This will print more information about the given exception

        :param Exception exception: the exception to handle
    """
    if isinstance(exception, HookError):
        write_error(exception)
        write_failure(exception.failure)
        abort(1)
    elif isinstance(exception, RadishError):
        write_error(handle_radish_errors(exception))
        abort(1)
    elif isinstance(exception, KeyboardInterrupt):
        console_write("Aborted by the user...")
        abort(1)
    else:
        write_error(exception)
        write_failure(Failure(exception))
        abort(2)


def handle_radish_errors(error_text):
    mapping = [
        {
            'class': FeatureFileSyntaxError,
            'text': 'You have a SyntaxError in your feature file! Please have a look into terraform-compliance and '
                    'radish documentation to find out which features are supported and how you could use them: '
                    'https://terraform-compliance.com  https://radish.readthedocs.io/en/stable/'
        },
        {
            'class': SameStepError,
            'text': '\n'.join(str(error_text).split('\n')[3:])
        },
        {
            'class': StepDefinitionNotFoundError,
            'text': '{}. Looks like a syntax error.'.format(str(error_text).split('\n')[3])
        },
    ]

    for map in mapping:
        if map['class'] is error_text.__class__:
            return map['text']

    return error_text
