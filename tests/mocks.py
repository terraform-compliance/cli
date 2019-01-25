from terraform_validate.terraform_validate import TerraformSyntaxException
from os import environ


class MockedData(object):

    # _change_value_in_dict() tests
    target_dictionary = dict(a=dict(b=dict(c='h', d='ello')))
    path_to_change_as_string = 'a.b'
    path_to_change_as_list = path_to_change_as_string.split('.')
    target_value = dict(e='test_value')
    expected_target_dictionary = dict(a=dict(b=dict(c='h', d='ello', e='test_value')))

    # enable_resource_mounting() tests
    mocked_tf_conf_for_mounting = {
        'resource': {
            'aws_security_group': {
                'default': {
                    'ingress': {
                        'to_port': '6666',
                        'from_port': '6666',
                        'protocol': 'tcp',
                        'security_groups': [
                            '${ var.security_groups }'
                        ]
                    },
                    'name': '${ module.label.id }',
                    'tags': '${ module.label.tags }',
                    'egress': {
                        'to_port': 0,
                        'cidr_blocks': [
                            '0.0.0.0/0'
                        ],
                        'from_port': 0,
                        'protocol': '-1'
                    },
                    'vpc_id': '${ var.vpc_id }',
                    'lifecycle': {
                        'create_before_destroy': True
                    },
                    'description': 'EFS'
                },
                'test_instance': {
                    'vpc_id': '${ var.vpc_id }',
                }
            },
            'aws_security_group_rule': {
                'test_ingress': {
                    'from_port': 0,
                    'protocol': '-1',
                    'to_port': 65535,
                    'security_group_id': '${ aws_security_group.test_instance.id }',
                    'cidr_blocks': [
                        '0.0.0.0/0'
                    ],
                    'type': 'ingress'
                },
                'test_egress': {
                    'from_port': 80,
                    'protocol': 'tcp',
                    'to_port': 80,
                    'security_group_id': '${ aws_security_group.test_instance.id }',
                    'cidr_blocks': [
                        '0.0.0.0/0'
                    ],
                    'type': 'egress'
                }
            }
        }
    }
    expected_tf_conf_for_mounting = {
        'resource': {
            'aws_security_group': {
                'default': {
                    'ingress': {
                        'to_port': '6666',
                        'from_port': '6666',
                        'protocol': 'tcp',
                        'security_groups': [
                            '${ var.security_groups }'
                        ]
                    },
                    'name': '${ module.label.id }',
                    'tags': '${ module.label.tags }',
                    'egress': {
                        'to_port': 0,
                        'cidr_blocks': [
                            '0.0.0.0/0'
                        ],
                        'from_port': 0,
                        'protocol': '-1'
                    },
                    'vpc_id': '${ var.vpc_id }',
                    'lifecycle': {
                        'create_before_destroy': True
                    },
                    'description': 'EFS'
                },
                'test_instance': {
                    'vpc_id': '${ var.vpc_id }',
                    'test_ingress': {
                        'from_port': 0,
                        'protocol': '-1',
                        'to_port': 65535,
                        'security_group_id': '${ aws_security_group.test_instance.id }',
                        'cidr_blocks': [
                            '0.0.0.0/0'
                        ],
                        'type': 'ingress'
                    },
                    'test_egress': {
                        'from_port': 80,
                        'protocol': 'tcp',
                        'to_port': 80,
                        'security_group_id': '${ aws_security_group.test_instance.id }',
                        'cidr_blocks': [
                            '0.0.0.0/0'
                        ],
                        'type': 'egress'
                    },
                    'ingress': [
                        {
                            'referred_name': 'test_ingress',
                            'from_port': 0,
                            'protocol': '-1',
                            'to_port': 65535,
                            'cidr_blocks': [
                                '0.0.0.0/0'
                            ],
                        }
                    ],
                    'egress':   [
                        {
                            'referred_name': 'test_egress',
                            'from_port': 80,
                            'protocol': 'tcp',
                            'to_port': 80,
                            'cidr_blocks': [
                                '0.0.0.0/0'
                            ],
                            }
                    ]
                }
            },
            'aws_security_group_rule': {
                'test_ingress': {
                    'from_port': 0,
                    'protocol': '-1',
                    'to_port': 65535,
                    'security_group_id': '${ aws_security_group.test_instance.id }',
                    'cidr_blocks': [
                        '0.0.0.0/0'
                    ],
                    'type': 'ingress'
                },
                'test_egress': {
                    'from_port': 80,
                    'protocol': 'tcp',
                    'to_port': 80,
                    'security_group_id': '${ aws_security_group.test_instance.id }',
                    'cidr_blocks': [
                        '0.0.0.0/0'
                    ],
                    'type': 'egress'
                }
            }
        }
    }
    mocked_tf_conf_with_no_mounting = {
        'resource': {
            'aws_security_group': {
                'default': {
                    'ingress': {
                        'to_port': '6666',
                        'from_port': '6666',
                        'protocol': 'tcp',
                        'security_groups': [
                            '${ var.security_groups }'
                        ]
                    },
                    'name': '${ module.label.id }',
                    'tags': '${ module.label.tags }',
                    'egress': {
                        'to_port': 0,
                        'cidr_blocks': [
                            '0.0.0.0/0'
                        ],
                        'from_port': 0,
                        'protocol': '-1'
                    },
                    'vpc_id': '${ var.vpc_id }',
                    'lifecycle': {
                        'create_before_destroy': True
                    },
                    'description': 'EFS'
                },
                'test_instance': {
                    'vpc_id': '${ var.vpc_id }',
                }
            },
            'aws_security_group_rule': {
                'test_ingress': {
                    'from_port': 0,
                    'protocol': '-1',
                    'to_port': 65535,
                    'cidr_blocks': [
                        '0.0.0.0/0'
                    ],
                    'type': 'ingress'
                },
                'test_egress': {
                    'from_port': 80,
                    'protocol': 'tcp',
                    'to_port': 80,
                    'cidr_blocks': [
                        '0.0.0.0/0'
                    ],
                    'type': 'egress'
                }
            }
        }
    }

    mocked_tf_issue_52 = ""

    # security_groups
    sg_ssh_with_2_cidrs = {u'to_port': 22, u'cidr_blocks': [u'213.86.221.35/32', u'195.99.231.117/32'], u'from_port': 22, u'protocol': u'tcp'}
    sg_ssh_with_2_cidrs_any_proto = {u'to_port': 22, u'cidr_blocks': [u'213.86.221.35/32', u'195.99.231.117/32'], u'from_port': 22, u'protocol': u'-1'}
    sg_ssh_with_all_ips = {u'to_port': 22, u'cidr_blocks': [u'0.0.0.0/0'], u'from_port': 22, u'protocol': u'tcp'}
    sg_all_port_all_ip = {u'to_port': 0, u'cidr_blocks': [u'0.0.0.0/0'], u'from_port': 0, u'protocol': u'tcp'}
    sg_all_port_no_ip = {}
    sg_invalid = {u'to_port': 1, u'from_port': 2}


    # refined sg_params
    sg_params_ssh_with_2_cidrs = dict(protocol=['tcp'], from_port=22, to_port=22, cidr_blocks=['213.86.221.35/32', '195.99.231.117/32'])
    sg_params_ssh_with_2_cidrs_any_proto = dict(protocol=['tcp', 'udp'], from_port=22, to_port=22, cidr_blocks=['213.86.221.35/32', '195.99.231.117/32'])
    sg_params_all_port_all_ip = dict(protocol=['tcp'], from_port=0, to_port=65535, cidr_blocks=['0.0.0.0/0'])
    sg_params_all_port_no_ip = dict(protocol=['tcp', 'udp'], from_port=0, to_port=65535, cidr_blocks=[])


class MockedValidator(object):
    def __init__(self, directory):
        global state_file

        if directory == 'valueerror':
            raise ValueError('detailed message')
        elif directory == 'syntaxexception':
            state_key = 'MockedValidator.state'
            state = environ.get(state_key, None)
            if state:
                pass
            else:
                environ[state_key] = '1'
                raise TerraformSyntaxException('detailed message')


class MockedStep(object):
    def __init__(self, no_init=None):
        self.context = MockedStepContext()
        self.sentence = 'Given I am a step'

        if no_init is None:
            self.parent = MockedParentStep()

    def skip(self):
        self.state = 'skipped'

class MockedParentStep(object):
    def __init__(self):
        self.all_steps = [MockedStep(no_init=True), MockedStep(no_init=True), MockedStep(no_init=True)]

class MockedStepContext(object):
    def __init__(self):
        self.stash = MockedWorldConfigTerraform()
        self.resource_type = 'aws_db_instance'


class MockedWorld(object):
    def __init__(self):
        self.config = MockedWorldConfig()


class MockedWorldConfig(object):
    def __init__(self):
        self.terraform = MockedWorldConfigTerraform()


class MockedWorldConfigTerraform(object):
    def __init__(self):
        self.terraform_config = {
            u'resource': {
                u'resource_type': {
                    u'resource_name': {
                        u'resource_property': u'resource_property_value',
                        u'tags': u'${module.tags.tags}'
                    }
                },
                u'aws_s3_bucket': {
                    u'aws_s3_bucket_name': {
                        u'resource_property': u'resource_property_value',
                        u'tags': u'${module.tags.tags}'
                    }
                }
            },
            u'provider': {
                u'aws': {}
            },
            u'something_else': {'something': 'else'}
        }
    def resources(self, name):
        return MockedTerraformResourceList(self.terraform_config['resource'][name])


class MockedTerraformPropertyList(object):
    def __init__(self):
        self.properties = [MockedTerraformProperty()]

    def should_equal(self, bool):
        return bool

    def should_match_regex(self, regex):
        return True

class MockedTerraformProperty(object):
    def __init__(self):
        self.property_value = 'test_value'
        self.resource_name = 'test_resource_name'
        self.resource_type = 'test_resource_type'
        self.property_name = 'test_name'

    def should_match_regex(self, regex):
        return True

class MockedTerraformResourceList(object):
    def __init__(self, type={}):
        self.resource_list = [type]
        self.properties = [MockedTerraformPropertyList()]

    def should_have_properties(self, key):
        if key is None:
            raise Exception('should_have_properties hit')

    def property(self, key):
        if key is None:
            raise Exception('property hit')
        self.properties = MockedTerraformPropertyList()
        return self.properties

    def should_match_regex(self, regex):
        return True

    def find_property(self, property):
        if property is None:
            return None

        return MockedTerraformResourceList()

    def with_property(self, property, key):
        if (property is None) or (key is None):
            return None

        return MockedTerraformPropertyList()

class MockedArgumentParser(object):
    def __init__(self, prog, description):
        self.prog = prog
        self.description = description

    def add_argument(self, long_param, short_param, **kwargs):
        self.long_param = long_param
        self.short_param = short_param
        for key, value in kwargs.items():
            setattr(self, key, value)

    def parse_known_args(self, namespace):
        return (None, '-v')


class MockedArgHandling(object):
    def __init__(self):
        self.ssh_key = '~/.ssh/private.key'
        self.features = '/path/to/features'
        self.tf_dir = '/path/to/terraform/files'
