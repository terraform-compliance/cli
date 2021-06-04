import os
import stat
import sys
import subprocess
import platform
import urllib.request
import tempfile
from shutil import unpack_archive
import re


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

            windows_executable = os.path.join(path, '{}.exe'.format(program))
            if is_exe(windows_executable):
                return windows_executable
    return None


def convert_terraform_plan_to_json(terraform_plan_file, terraform_executable=None):
    print('. Converting terraform plan file.')
    if terraform_executable is None:
        terraform_executable = which('terraform')
    else:
        print('. Using {} as terraform executable.'.format(terraform_executable))

    if terraform_executable is None:
        sys.stderr.write('ERROR: Could not find "terraform" executable in PATH. Please either use "-t" parameter '
                         'or add terraform executable to your PATH.\n')
        sys.exit(1)

    path = os.path.dirname(terraform_plan_file)
    cwd = os.getcwd()
    os.chdir(path)

    try:
        with open('{}.json'.format(terraform_plan_file), 'w', encoding='utf-8') as FP_plan_file:
            terraform = subprocess.run([terraform_executable, 'show', '-json', terraform_plan_file],
                                       universal_newlines=True,
                                       stdout=FP_plan_file,
                                       stderr=subprocess.PIPE)
    except FileNotFoundError as err:
        sys.stderr.write(
            'ERROR: {} does not exist. Please give correct executable for "terraform".\n'.format(terraform_executable))
        sys.stderr.write('       {}\n'.format(str(err)))
        sys.exit(1)
    except PermissionError  as err:
        sys.stderr.write('ERROR: {} is not executable. Please give correct executable for "terraform".\n'.format(
            terraform_executable))
        sys.stderr.write('       {}\n'.format(str(err)))
        sys.exit(1)
    except OSError as err:
        sys.stderr.write(
            'ERROR: {} does not look like terraform. Please give correct executable for "terraform".\n'.format(
                terraform_executable))
        sys.stderr.write('       {}\n'.format(str(err)))
        sys.exit(1)

    os.chdir(cwd)

    if terraform.returncode == 0:
        return '{}.json'.format(terraform_plan_file)

    # Ok here we are going to fail because plan file has been created by a different terraform
    # So, we will attempt a detection of terraform version here. Hoping that the terraform stderr
    # about this error will not change in the future.
    target_version, current_version = detect_required_terraform_version(terraform.stderr)

    if current_version is not None and target_version is not None:
        sys.stderr.write('. Plan file has been created by terraform v{}, '
                         'but you have v{}\n'.format(target_version, current_version))
        terraform_executable = download_terraform(target_version)
        return convert_terraform_plan_to_json(terraform_plan_file=terraform_plan_file,
                                              terraform_executable=terraform_executable)


    else:
        sys.stderr.write('ERROR: Failed to convert terraform plan file to JSON format via terraform. Here is the error :\n')
        print(terraform.stdout)
        print(terraform.stderr)

        if 'Could not satisfy plugin requirements' in terraform.stderr:
            print('Hint: You can avoid this problem by converting your plan file to a JSON file via running;\n '
                  '\n    # terraform show -json {} > {}.json'
                  '\n\n                          OR'
                  '\n    # terraform init'
                  '\n\n in {} directory and then pass (with -p) {}.json to terraform-compliance'.format(terraform_plan_file,
                                                                                                        terraform_plan_file,
                                                                                                        path,
                                                                                                        terraform_plan_file))

        sys.exit(1)


def get_platform_details():
    system = platform.system().lower()
    arch = "amd64" if platform.machine() == "x86_64" else "386"
    return system, arch


def download_terraform(version):
    system, arch = get_platform_details()
    tmp_dir = tempfile.gettempdir()
    terraform_file = "{}/terraform_{}_{}_{}".format(tmp_dir, version, system, arch)

    if os.path.isfile(terraform_file):
        print('. Using cached {}'.format(terraform_file))
        return terraform_file

    url = 'https://releases.hashicorp.com/terraform/{}/terraform_{}_{}_{}.zip'.format(version, version, system,
                                                                                      arch)
    print('. Downloading terraform v{} from {} ...'.format(version, url))
    urllib.request.urlretrieve(url, '{}.zip'.format(terraform_file))
    print('. Unpacking {}.zip'.format(terraform_file))
    unpack_archive('{}.zip'.format(terraform_file), tmp_dir)
    os.rename('{}/terraform'.format(tmp_dir), terraform_file)
    st = os.stat(terraform_file)
    os.chmod(terraform_file, st.st_mode | stat.S_IEXEC)
    return terraform_file


def detect_required_terraform_version(string):
    match_regex = [
        r'([0-9.]+), but this is ([0-9.]+); plan files cannot be transferred between',
        r'by Terraform v([0-9.]+), which is newer than current v([0-9.]+);'
    ]
    for pattern in match_regex:
        match = re.search(pattern, string, re.DOTALL)

        if match is not None:
            return match.group(1), match.group(2)

    return None, None