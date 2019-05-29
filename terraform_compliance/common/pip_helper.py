import subprocess
from sys import exit, executable


def reinstall_radish():
    def pip(action, package, params=None):
        print('{}ing {}..'.format(action, package))

        if action == 'uninstall':
            cmds = [executable, "-m", "pip", action, '--yes', package]
        else:
            cmds = [executable, "-m", "pip", action, package]

        subprocess.call(cmds)

    print("Fixing the problem on radish and radish-bdd")
    pip('uninstall', 'radish-bdd')
    pip('uninstall', 'radish')
    pip('install', 'radish==0.1.10')
    pip('install', 'radish-bdd==0.8.6')

    print("~"*40)
    print(" Please run terraform-compliance again.")
    print("~"*40)
    exit(1)
