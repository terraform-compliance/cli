"""
BDD test framework for terraform
"""
from setuptools import find_packages, setup
from terraform_compliance.main import __app_name__, __version__
import radish

dependencies = [
    'radish',
    'radish-bdd',
    'gitpython',
    'netaddr',
    'colorful',
    'filetype'
]

setup(
    name=__app_name__,
    version=__version__,
    url='https://github.com/eerkunt/terraform-compliance',
    license='MIT',
    author='Emre Erkunt',
    author_email='emre.erkunt@gmail.com',
    description='BDD test framework for terraform',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'terraform-compliance=terraform_compliance.main:cli',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
