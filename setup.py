"""
BDD test framework for terraform
"""
from setuptools import find_packages, setup
from terraform_compliance import __app_name__, __version__


dependencies = [
    'radish-bdd==0.13.1',
    'gitpython==3.1.20',
    'netaddr==0.8.0',
    'colorful==0.5.4',
    'filetype==1.1.0',
    'junit-xml==1.9',
    'emoji==2.1.0',
    'lxml==4.9.1',
    'semver==2.13.0',
    'IPython==7.16.1',
    'orjson==3.8.3',
    'diskcache==5.4.0'
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    extras_require = {
        "faster_parsing": ["orjson"],
    }
)
