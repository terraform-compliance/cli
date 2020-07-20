import json
import re
from IPython import embed
from radish import before, after, world
from terraform_compliance.extensions.terraform import TerraformParser
from terraform_compliance.common.helper import Null

@before.each_feature
def load_terraform_data(feature):
    world.config.terraform = TerraformParser(world.config.user_data['plan_file'])


@before.each_step
def parse_curly_braces(step):

    # BEFORE START
    # ignore given steps (doesn't support match, would need to do something else for them, also there's no second stash)
    # ignore steps that doesn't use this feature
    if step.context_class == 'given':
        return

    # if step doesn't have argument_match, it doesn't support in_step_variables
    if step.argument_match is None:
        return

    if step.context.bad_tags:
        return

    # name_fields = step.argument_match.match.parser._named_fields
    groupindex = dict(step.argument_match.match.match.re.groupindex)
    regs = step.argument_match.match.match.regs
    sentence = step.context_sensitive_sentence
    field_map = {field: sentence[regs[i][0]: regs[i][1]] for field, i in groupindex.items()}

    # ignore the regex statements
    if 'search_regex' in field_map:
        del field_map['search_regex']

    in_step_variables = {}
    match = step.context.match
    # regex = r'{(.*)}'
    regex = r'(.*){(.*)}(.*)'

    for field, field_val in field_map.items():
        matches = match.regex_match(regex, str(field_val))
        if matches is None:
            continue
        
        query = matches.group(2).split('.')
        if not query:
            continue # do something here
        
        resource_type = query.pop(0)

        # query_result = match.get(step.cumulative_stash, resource_type)
        query_result = [resource for resource in step.context.cumulative_stash if match.equals(resource['type'], resource_type)]
        for q in query:
            if not query_result:
                break
            query_result = [match.get(resource, q) for resource in query_result if match.contains(resource, q)]
        

        if matches.group(1) or matches.group(3):
            if not all(isinstance(resource, (str, bool, int, float)) for resource in query_result):
                raise TypeError("Improper in step variable usage. Can't mix affixes with non-str in step variabes.")
            
            query_result = [f'{matches.group(1)}{resource}{matches.group(3)}' for resource in query_result]

        in_step_variables[field] = query_result

        '''
        if {} in field_val:
            regex match field_val
            enforce that there're only 2 groups (1 {}) (ignoring filtering for now)
            get the string that represents aws_lambda_function.name
            split it from .'s
            dereference the second_stash

            (enforce JSON vs string?)            
            add the result into in_step_variables

        '''
        
    step.context.in_step_variables = in_step_variables


# debugging step should be always the last hooker
@after.each_step
def wait_for_user_input(step):
    if world.config.user_data['debugging_mode_enabled'] == 'False':
        return

    cmd = 'cmd'
    while cmd != '':
        try:
            cmd = input(">> Press enter to continue")
        except EOFError:
            print()
            return
        
        if cmd == 'd':
            embed()
        elif cmd == 's':
            print(json.dumps(step.context.stash, indent=4))
        elif cmd != '':
            print(
                """
Commands
- s: prints stash
- d: opens Interactive Python
- h: prints commands
                """
            )


