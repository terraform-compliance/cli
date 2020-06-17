import colorful
from radish.utils import console_write
from radish import custom_type
from radish import world
from terraform_compliance.common.defaults import Defaults
from terraform_compliance.common.error_handling import Error


def skip_step(step, resource=None, message=None):
    if resource is None:
        resource = 'any'

    if message is None:
        message = '{} {} {}'.format(Defaults().yellow('Can not find'),
                                    Defaults().green(resource),
                                    Defaults().yellow('defined in target terraform plan.'))
        e_message = 'Can not find {} defined in target terraform plan.'.format(resource)
    else:
        e_message = message
        message = Defaults().yellow(message)


    if step.context.no_skip:
        if -1 in step.context.lines_to_noskip or step.line in step.context.lines_to_noskip:
            message = Defaults().failure_colour(message)
            Error(step, e_message)
            return
    
    if str(world.config.formatter) in ('gherkin'):
        console_write("\t{} {}: {}".format(Defaults().info_icon,
                                           Defaults().skip_colour('SKIPPING'),
                                           message.format(resource=Defaults().green(resource)))
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


@custom_type("ANY", r".+")
def custom_type_any(text):
    return text.replace('"', '').replace('\'', '')


@custom_type("PROPERTY", r"(\"[\s\*\.\/_\-A-Za-z0-9:\(\)\[\]\']+\")|"
                         r"([\*\.\/_\-A-Za-z0-9:\(\)\[\]\']+)")
def custom_type_prop(text):
    return text.replace('"', '').replace('\'', '')

@custom_type("PROPERTY_COMPAT", r"([\*\.\/_\-A-Za-z0-9:\(\)\[\]\']+\s[\*\.\/_\-A-Za-z0-9:\(\)\[\]\']+$)|"
                                r"(\"[\s\*\.\/_\-A-Za-z0-9:\(\)\[\]\']+\"$)|"
                                r"([\*\.\/_\-A-Za-z0-9:\(\)\[\]\']+$)")
def custom_type_prop(text):
    return text.replace('"', '').replace('\'', '')

@custom_type("SECTION", r"[\"'a-z]+")
def custom_type_section(text):
    if text in ['resource', 'provider', 'data', 'variable',
                'resources', 'providers', 'datas', 'variables']:
        return text.replace('"', '').replace('\'', '')


@custom_type("CONDITION", r"[\"'a-z]+")
def custom_type_condition(text):
    if text in ['only', 'not']:
        return text.replace('"', '').replace('\'', '')
