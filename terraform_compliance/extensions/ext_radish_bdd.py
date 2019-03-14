import colorful
from radish.utils import console_write


def skip_step(step, resource=None, message=None):
    if resource is None:
        resource = 'any'

    if message is None:
        message = '{} {} {}'.format(colorful.orange('Can not find'),
                                    colorful.magenta(resource),
                                    colorful.orange('defined in target terraform files.'))
    else:
        message = colorful.orange(message)

    console_write("\t{}: {}".format(colorful.bold_purple('SKIPPING'),
                                    message.format(resource=colorful.magenta(resource)))
    )
    step.skip()

    # Skip all steps in the scenario
    for each in step.parent.all_steps:
        each.runable = False


def step_condition(step):
    current_condition = step.sentence.lower().split(" ")[0]

    # if the condition is AND then check for the first previous feature line to determine if it is a
    # GIVEN, WHEN or THEN
    if current_condition == "and":
        step_id = int(step.id)-1
        if step_id > 0:
            for parent_step in step.parent.all_steps.reverse():
                # For the steps that has lower id than ours, so the steps on the above, not below
                if parent_step.id < step_id and parent_step.context_class in ["given", "when", "then"]:
                        current_condition = parent_step.context_class

    return current_condition


def write_stdout(level, message):

    prefix = colorful.bold_yellow(u'\u229b INFO :')
    if level == 'WARNING':
        prefix = colorful.bold_red(u'\u2757 WARNING :')
        message = colorful.yellow(message)


    added_prefix = u'\n\t\t{}\t{} '.format(colorful.gray(u'\u2502'),' '*len(prefix))
    message = message.split('\n')

    print(u'\t\t\u251c\u2501\t{} {}'.format(prefix, added_prefix.join(message)).encode('utf-8'))
