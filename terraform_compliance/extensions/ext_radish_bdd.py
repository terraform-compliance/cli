import colorful
from radish.utils import console_write


def skip_step(step, resource=None, message=None):
    if resource is None:
        resource = 'any'

    if message is None:
        message = '{} {} {}'.format(colorful.orange('Can not find'),
                                    colorful.magenta(resource),
                                    colorful.orange('resource defined in target terraform files.'))
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
                if parent_step.id < step_id:
                    if parent_step.sentence.lower().split(" ")[0] in ["given", "when", "then"]:
                        current_condition = parent_step.sentence.lower().split(" ")[0]

    return current_condition
