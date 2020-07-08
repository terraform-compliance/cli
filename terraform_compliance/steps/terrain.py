import curses
import json
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

    # pythonify this later
    while cmd != '':
        try:
            cmd = input(">> Press enter to continue")
        except EOFError:
            print()
            return
        
        if cmd == 'd':
            try:
                from IPython import embed
            except ImportError as e:
                raise RadishError(
                'if you want to use the failure inspector extension you have to "pip install radish-bdd[ipython-debugger]"'
                )

            embed()
        elif cmd == 's':
            # print(step.context.stash)
            print(json.dumps(step.context.stash, indent=4))
        elif cmd != '':
            print(
                """
Commands
- s: prints stash
- d: opens interactive python
                """
            )


