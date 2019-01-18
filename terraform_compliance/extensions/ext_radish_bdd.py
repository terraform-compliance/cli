import colorful
from radish.utils import console_write


def skip_step(step, resource=None, message=None):
    step.skip()
    if resource is None:
        resource = 'any'

    if message is None:
        message = '{} {} {}'.format(colorful.orange('Can not find'),
                                    colorful.magenta(resource),
                                    colorful.orange('resource defined in target terraform files.'))
    else:
        message = colorful.orange(message)

    console_write("\t{}: {}".format(colorful.bold_purple('SKIPPING'),
                                    message)
    )
