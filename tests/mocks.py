

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