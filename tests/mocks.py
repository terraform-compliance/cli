from terraform_compliance.common.helper import Match


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

    mocked_plan_outputs = {
        "security_group_mounting": {"format_version":"0.1","terraform_version":"0.12.0","variables":{"environment":{"value":"supp"},"server_port":{"value":8080}},"planned_values":{"root_module":{"resources":[{"address":"aws_security_group.example","mode":"managed","type":"aws_security_group","name":"example","provider_name":"aws","schema_version":1,"values":{"description":"Managed by Terraform","egress":[{"cidr_blocks":["0.0.0.0/0"],"description":"","from_port":3,"ipv6_cidr_blocks":[],"prefix_list_ids":[],"protocol":"tcp","security_groups":[],"self":True,"to_port":8080}],"name_prefix":None,"revoke_rules_on_delete":False,"tags":None,"timeouts":None}},{"address":"aws_security_group_rule.example_rule[0]","mode":"managed","type":"aws_security_group_rule","name":"example_rule","index":0,"provider_name":"aws","schema_version":2,"values":{"cidr_blocks":["172.23.204.0/23","172.23.208.0/21","172.23.96.0/21","55.0.0.0/14","10.0.0.0/8"],"description":None,"from_port":8080,"ipv6_cidr_blocks":None,"prefix_list_ids":None,"protocol":"tcp","self":False,"to_port":8081,"type":"ingress"}}]}},"resource_changes":[{"address":"aws_security_group.example","mode":"managed","type":"aws_security_group","name":"example","provider_name":"aws","change":{"actions":["create"],"before":None,"after":{"description":"Managed by Terraform","egress":[{"cidr_blocks":["0.0.0.0/0"],"description":"","from_port":3,"ipv6_cidr_blocks":[],"prefix_list_ids":[],"protocol":"tcp","security_groups":[],"self":True,"to_port":8080}],"name_prefix":None,"revoke_rules_on_delete":False,"tags":None,"timeouts":None},"after_unknown":{"arn":True,"description":False,"egress":[{"cidr_blocks":[False],"description":False,"from_port":False,"ipv6_cidr_blocks":False,"prefix_list_ids":False,"protocol":False,"security_groups":False,"self":False,"to_port":False}],"id":True,"ingress":True,"name":True,"name_prefix":False,"owner_id":True,"revoke_rules_on_delete":False,"tags":False,"timeouts":False,"vpc_id":True}}},{"address":"aws_security_group_rule.example_rule[0]","mode":"managed","type":"aws_security_group_rule","name":"example_rule","index":0,"provider_name":"aws","change":{"actions":["create"],"before":None,"after":{"cidr_blocks":["172.23.204.0/23","172.23.208.0/21","172.23.96.0/21","55.0.0.0/14","10.0.0.0/8"],"description":None,"from_port":8080,"ipv6_cidr_blocks":None,"prefix_list_ids":None,"protocol":"tcp","self":False,"to_port":8081,"type":"ingress"},"after_unknown":{"cidr_blocks":[False,False,False,False,False],"description":False,"from_port":False,"id":True,"ipv6_cidr_blocks":False,"prefix_list_ids":False,"protocol":False,"security_group_id":True,"self":False,"source_security_group_id":True,"to_port":False,"type":False}}}],"configuration":{"root_module":{"resources":[{"address":"aws_security_group.example","mode":"managed","type":"aws_security_group","name":"example","provider_config_key":"aws","schema_version":1},{"address":"aws_security_group_rule.example_rule","mode":"managed","type":"aws_security_group_rule","name":"example_rule","provider_config_key":"aws","expressions":{"cidr_blocks":{"constant_value":["172.23.204.0/23","172.23.208.0/21","172.23.96.0/21","55.0.0.0/14","10.0.0.0/8"]},"from_port":{"references":["var.server_port"]},"protocol":{"constant_value":"tcp"},"security_group_id":{"references":["aws_security_group.example"]},"to_port":{"references":["var.server_port"]},"type":{"constant_value":"egress"}},"schema_version":2,"count_expression":{"references":["var.environment"]}}],"variables":{"environment":{"default":"supp"},"server_port":{"default":8080,"description":"The port the server will use for HTTP requests"}}}}}
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
    sg_params_all_port_all_ip = dict(protocol=['tcp'], from_port=1, to_port=65535, cidr_blocks=['0.0.0.0/0'])
    sg_params_all_port_no_ip = dict(protocol=['tcp', 'udp'], from_port=1, to_port=65535, cidr_blocks=[])
    sg_params_list_range_public = dict(protocol=['tcp'], from_port=22, to_port=80, cidr_blocks=['0.0.0.0/0'])
    sg_params_list_range_private = dict(protocol=['tcp'], from_port=22, to_port=80, cidr_blocks=['192.168.0.0/23'])


class MockedStep(object):
    def __init__(self, no_init=None):
        self.context = MockedStepContext()
        self.sentence = 'Given I am a step'
        self.context_sensitive_sentence = self.sentence
        self.state = 'passed'
        self.id = 0
        self.all_tags = [MockedTags()]

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
        self.name = ''
        self.addresses = 'aws_db_instance.something'
        self.property_name = 'mocked_property'
        self.no_failure = False
        self.no_skip = False
        self.failure_class = 'no_name'
        self.match = Match(case_sensitive=False)


class MockedWorld(object):
    def __init__(self):
        self.config = MockedWorldConfig()


class MockedWorldConfig(object):
    user_data = dict(
        exit_on_failure=True,
        no_failure=False
    )
    def __init__(self):
        self.terraform = MockedWorldConfigTerraform()
        self.formatter = 'gherkin'
        self.user_data = dict(
            exit_on_failure=True,
            no_failure=False
        )


class MockedWorldConfigTerraform(object):
    def __init__(self):
        self.resources = {
            'provider_type_id': {
                'type': 'resource_type_supports_tags',
                'address': 'provider_type_id',
                'mode': 'managed',
                'values': {
                    'tags': {
                        'some': 'tags',
                        'some_other': 'other_tags'
                    },
                    'some_key': 'some_value'
                }
            },
            'provider_type_id_without_tags': {
                'type': 'resource_type_without_tags',
                'address': 'provider_type_id_without_tags',
                'mode': 'managed',
                'values': {}
            }
        }
        self.resources_raw = self.resources
        self.variables = {
            'some_variable': 'some_value',
            'some_other_variable': 'some_other_value'
        }
        self.configuration = {
            'providers' : {
                'some_provider.some_provider_alias': {
                    'name': 'some_provider',
                    'alias': 'some_provider_alias',
                    'some_provider': 'some_provider_value'
                }
            }
        }

    def find_resources_by_type(self, resource_type, match=None):
        for key, value in self.resources.items():
            if value['type'] == resource_type and value['mode'] == 'managed':
                return [value]

    def get_providers_from_configuration(self, provider_type, match=None):
        if provider_type == 'some_provider':
            return ['some_provider']

        return []


class MockedTerraformPropertyList(object):
    def __init__(self):
        self.properties = [MockedTerraformProperty()]

    def should_equal(self, boolMockedTerraformResourceList):
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
        self.enable_modules = False


class MockedTerraformResource(object):
    def __init__(self):
        self.config = {"count": 2}


class MockedTags(object):
    def __init__(self, name='no_name'):
        self.name = name
