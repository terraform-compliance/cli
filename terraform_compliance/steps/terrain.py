import curses
import json
from IPython import embed
from radish import before, after, world
from terraform_compliance.extensions.terraform import TerraformParser
from terraform_compliance.main import cli_arguments

@before.each_feature
def load_terraform_data(feature):
    world.config.terraform = TerraformParser(world.config.user_data['plan_file'])


@after.each_step
def wait_for_user_input(step):
    global cli_arguments

    if not cli_arguments.debug:
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


