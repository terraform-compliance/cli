import os
import sys
import subprocess


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def convert_terraform_plan_to_json(terraform_plan_file, terraform_executable=None):
    print('. Converting terraform plan file.')
    if terraform_executable is None:
        terraform_executable = which('terraform')

    path = os.path.dirname(terraform_plan_file)

    cwd = os.getcwd()
    os.chdir(path)
    with open('{}.json'.format(terraform_plan_file), 'w') as FP_plan_file:
        terraform = subprocess.run([terraform_executable, 'show', '-json', terraform_plan_file],
                                   universal_newlines=True,
                                   stdout=FP_plan_file,
                                   stderr=subprocess.PIPE)

    os.chdir(cwd)

    if terraform.returncode == 0:
        return '{}.json'.format(terraform_plan_file)

    print('ERROR: Failed to convert terraform plan file to JSON format via terraform. Here is the error :')
    print(terraform.stdout)
    print(terraform.stderr)
    sys.exit(1)
