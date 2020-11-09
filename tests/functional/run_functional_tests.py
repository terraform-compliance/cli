import os
import sys
import subprocess
import colorful
import re


class Config(object):
    test_dir = 'tests/functional'
    default_parameters = [
        '--no-ansi'
    ]



if len(sys.argv) == 2:
    print('Running functional tests in {}.'.format(sys.argv[1]))
    tests = [sys.argv[1]]
else:
    print('Running functional tests in {}.'.format(Config.test_dir))
    tests = []
    for x in os.listdir(Config.test_dir):
        if os.path.isdir('{}/{}'.format(Config.test_dir, x)):
            tests.append(x)

print('Total {} number of tests will be executed.'.format(len(tests)))

test_summary = []
failure_happened = False

for test_dir in tests:
    parameters = ['terraform-compliance']
    parameters.extend(Config.default_parameters.copy())
    directory = '{}/{}'.format(Config.test_dir, test_dir)

    test_result = ''
    expected = ''
    unexpected = ''

    if not os.path.isfile('{}/plan.out.json'.format(directory)) or not os.path.isfile('{}/test.feature'.format(directory)):
        test_result = colorful.orange('skipped')
    else:
        if os.path.isfile('{}/.failure'.format(directory)):
            parameters.append('--wip')

        if os.path.isfile('{}/.expected'.format(directory)):
            with open('{}/.expected'.format(directory)) as expected_file:
                expected = expected_file.read().split('\n')

        if os.path.isfile('{}/.unexpected'.format(directory)):
            with open('{}/.unexpected'.format(directory)) as unexpected_file:
                unexpected = unexpected_file.read().split('\n')

        if not os.path.isfile('{}/.no_early_exit'.format(directory)):
            parameters.append('-q')

        parameters.extend([
            '-f', '{}'.format(directory),
            '-p', '{}/plan.out.json'.format(directory)
        ])

        try:
            print('Running {}.'.format(colorful.yellow(test_dir)))
            # TODO: Add multithreading here if we have more than 50+ integration tests ?
            test_process = subprocess.run(parameters,
                                          check=True,
                                          # shell=True,
                                          stdout=subprocess.PIPE,
                                          universal_newlines=True,
                                          )

            if os.environ.get('DEBUG'):
                print('Output: {}'.format(colorful.grey(test_process.stdout)))

            if test_process.returncode == 0:
                if expected:
                    expected_failures = [
                        exp for exp in expected 
                        if not re.findall(exp, str(test_process.stdout), re.A)
                    ]

                    if expected_failures:
                        print('\nOutput: {}'.format(test_process.stdout))
                        print('Can not find ;')
                        for failure in expected_failures:
                            print('\t{}'.format(colorful.yellow(failure)))
                        print('in the test output.\n')

                        test_result = colorful.red('failed')
                        failure_happened = True

                if unexpected:
                    unexpected_failures = [
                        unexp for unexp in unexpected 
                        if re.findall(unexp, str(test_process.stdout))
                    ]

                    if unexpected_failures:
                        print('\nOutput: {}'.format(test_process.stdout))
                        print('Found;')
                        for failure in expected_failures:
                            print('\t{}'.format(colorful.yellow(failure)))
                        print('in the test output. This was unexpected.\n')

                        test_result = colorful.red('failed')
                        failure_happened = True
                
                if not failure_happened:
                    test_result = colorful.green('passed')

            else:
                print('Output: {}'.format(test_process.stdout))
                test_result = colorful.red('failed')
                failure_happened = True

        except subprocess.CalledProcessError as e:
            failure_happened = True

            if e.returncode != 1:
                test_result = colorful.orange('errored')
            else:
                test_result = colorful.red('failed')
                print('Expected a different return code. Received {}'.format(colorful.yellow(e.returncode)))

            print('Output: {}'.format(e.stdout))

    test_summary.append('{:.<70s}{:.>10s}'.format(test_dir, test_result))

print('\n\nRan {} tests.'.format(len(tests)))
print('\n'.join(sorted(test_summary)))

if failure_happened:
    sys.exit(1)
