from unittest import TestCase
from terraform_compliance.steps.steps import (
    i_have_name_section_configured,
    i_action_them,
    i_expect_the_result_is_operator_than_number,
    it_contains_something_old,
    property_is_enabled,
    its_value_condition_match_the_search_regex_regex,
    it_condition_have_proto_protocol_and_port_port_for_cidr,
    it_fails,
    its_key_is_value, its_key_is_not_value,
    its_key_metadata_has_something,
    its_value_condition_equal,
    its_value_condition_contain,
    it_must_contain_something
)
from terraform_compliance.common.exceptions import TerraformComplianceNotImplemented, Failure
from tests.mocks import MockedStep, MockedWorld
from mock import patch


class TestStepCases(TestCase):

    def test_i_have_name_section_configured_type_not_found(self):
        step = MockedStep()
        with self.assertRaises(AssertionError) as err:
            i_have_name_section_configured(step, 'some_name', 'some_invalid_type', 'some_world')

        self.assertEqual(str(err.exception), 'some_invalid_type configuration type does not exist or not implemented '
                                             'yet. Use resource(s), provider(s), variable(s), output(s) or data(s) '
                                             'instead.')

    def test_i_have_name_section_configured_resource_that_supports_tags_found(self):
        step = MockedStep()
        world = MockedWorld()
        name = 'resource that supports tags'
        type_name = 'resource'

        self.assertTrue(i_have_name_section_configured(step, name, type_name, world))
        self.assertEqual(step.context.name, name)
        self.assertEqual(step.context.type, type_name)

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_i_have_name_section_configured_resource_that_supports_tags_not_found(self, *args):
        step = MockedStep()
        world = MockedWorld()
        del world.config.terraform.resources['provider_type_id']
        name = 'resource that supports tags'
        type_name = 'resource'

        self.assertIsNone(i_have_name_section_configured(step, name, type_name, world))
        self.assertEqual(step.state, 'skipped')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_i_have_name_section_configured_resource_not_found(self, *args):
        step = MockedStep()
        world = MockedWorld()
        name = 'non_existent_resource_id'
        type_name = 'resource'

        self.assertIsNone(i_have_name_section_configured(step, name, type_name, world))
        self.assertEqual(step.state, 'skipped')

    def test_i_have_name_section_configured_resource_found(self):
        step = MockedStep()
        world = MockedWorld()
        name = 'resource_type_without_tags'
        type_name = 'resource'

        self.assertTrue(i_have_name_section_configured(step, name, type_name, world))

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_i_have_name_section_configured_variable_not_found(self, *args):
        step = MockedStep()
        world = MockedWorld()
        name = 'non_existent_variable'
        type_name = 'variable'

        self.assertIsNone(i_have_name_section_configured(step, name, type_name, world))
        self.assertEqual(step.state, 'skipped')

    def test_i_have_name_section_configured_variable_found(self):
        step = MockedStep()
        world = MockedWorld()
        name = 'some_variable'
        type_name = 'variables'

        self.assertTrue(i_have_name_section_configured(step, name, type_name, world))

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_i_have_name_section_configured_provider_not_found(self, *args):
        step = MockedStep()
        world = MockedWorld()
        name = 'non_existing_provider'
        type_name = 'provider'

        self.assertIsNone(i_have_name_section_configured(step, name, type_name, world))
        self.assertEqual(step.state, 'skipped')

    def test_i_have_name_section_configured_provider_found(self):
        step = MockedStep()
        world = MockedWorld()
        name = 'some_provider'
        type_name = 'providers'

        self.assertTrue(i_have_name_section_configured(step, name, type_name, world))

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_it_condition_contain_something_resource_is_not_dict_failure(self, *args):
        step = MockedStep()
        step.context_sensitive_sentence = 'it must contain something'
        step.context.type = 'resource'
        step.context.stash = ['some_resource']
        with self.assertRaises(Failure):
            self.assertIsNone(it_must_contain_something(step, 'something'))

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_it_condition_contain_something_resource_not_found(self, *args):
        step = MockedStep()
        step.context_sensitive_sentence = 'it must contain something'
        step.context.type = 'resource'
        step.context.stash = [
            {
                'address': 'some_address',
                'type': 'resource',
                'values': {
                    'something': True
                }
            }
        ]
        with self.assertRaises(Failure) as err:
            self.assertIsNone(it_must_contain_something(step, 'something else'))
        self.assertEqual(str(err.exception), '{} ({}) does not have {} property.'.format('some_address',
                                                                                         'resource',
                                                                                         'something else'))

    @patch('terraform_compliance.extensions.ext_radish_bdd', return_value=None)
    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_it_condition_contain_something_resource_not_found_skip_step(self, *args):
        step = MockedStep()
        step.context_sensitive_sentence = 'it contains something'
        step.context.type = 'resource'
        step.context.stash = [
            {
                'address': 'some_address',
                'type': 'resource',
                'values': {
                    'something': True
                }
            }
        ]

        self.assertIsNone(it_contains_something_old(step, 'something else'))

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_it_condition_contain_something_resource_found(self, *args):
        step = MockedStep()
        step.context_sensitive_sentence = 'it contains something'
        step.context.type = 'resource'
        step.context.stash = [
            {
                'address': 'some_address',
                'type': 'resource',
                'values': {
                    'something': True
                }
            }
        ]

        self.assertTrue(it_contains_something_old(step, 'something'))

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_it_condition_contain_something_resource_value_is_list(self, *args):
        step = MockedStep()
        step.context_sensitive_sentence = 'it contains something'
        step.context.type = 'resource'
        step.context.stash = [
            {
                'address': 'some_address',
                'type': 'resource',
                'values': [
                    {
                        'key': 'something',
                        'value': 'some_value'
                    }
                ]
            }
        ]

        self.assertTrue(it_contains_something_old(step, 'something'))

    @patch('terraform_compliance.steps.then.it_must_contain_something.seek_key_in_dict', return_value=None)
    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_it_condition_contain_something_provider_not_found(self, *args):
        step = MockedStep()
        step.context.type = 'provider'
        step.context.stash = []

        self.assertIsNone(it_contains_something_old(step, 'something'))

    @patch('terraform_compliance.steps.then.it_must_contain_something.seek_key_in_dict', return_value=True)
    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_it_condition_contain_something_provider_found(self, *args):
        step = MockedStep()
        step.context.type = 'provider'
        step.context.stash = [{'name': 'test'}]

        self.assertTrue(it_contains_something_old(step, 'name'))

    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_property_is_enabled_not_implemented(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'something'
            }
        ]
        with self.assertRaises(Failure):
            property_is_enabled(step, 'something')

    def test_property_is_enabled_success(self):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'values': {
                    'storage_encrypted': True
                }
            }
        ]
        self.assertTrue(property_is_enabled(step, 'storage_encrypted'))

    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_property_is_enabled_failure(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'address': 'resource',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        with self.assertRaises(Failure):
            property_is_enabled(step, 'storage_encrypted')

    def test_it_condition_have_proto_protocol_and_port_port_for_cidr_ports_must_only_success(self):
        step = MockedStep()
        step.context.stash = []
        condition = 'not important'
        proto = 'not important'
        port = '1-2'
        cidr = 'not important'
        self.assertTrue(it_condition_have_proto_protocol_and_port_port_for_cidr(step, condition, proto, port, cidr))

    def test_it_condition_have_proto_protocol_and_port_port_for_cidr_ports_with_comma_must_only_success(self):
        step = MockedStep()
        step.context.stash = []
        condition = 'not important'
        proto = 'not important'
        port = '1,2'
        cidr = 'not important'
        self.assertTrue(it_condition_have_proto_protocol_and_port_port_for_cidr(step, condition, proto, port, cidr))

    def test_it_condition_have_proto_protocol_and_port_port_for_cidr_port_success(self):
        step = MockedStep()
        step.context.stash = []
        condition = 'not important'
        proto = 'not important'
        port = '1'
        cidr = 'not important'
        self.assertTrue(it_condition_have_proto_protocol_and_port_port_for_cidr(step, condition, proto, port, cidr))

    def test_i_action_them_count_list_of_list(self):
        step = MockedStep()
        step.context.stash = [1,2,3]
        i_action_them(step, 'count')
        self.assertEqual(step.context.stash, {'values': 3})

    def test_i_action_them_count_list_of_dict_with_resources(self):
        step = MockedStep()
        step.context.stash = [
            {
                'values': {
                    'first': True
                }
            },
            {
                'values': {
                    'second': True
                }
            },
            {
                'values': {
                    'third': True
                }
            }
        ]
        i_action_them(step, 'count')
        self.assertEqual(step.context.stash, {'values': 3})

    def test_i_action_them_count_list_of_dict_with_properties(self):
        step = MockedStep()
        step.context.stash = [{},{},{}]
        step.context.property_name = 'resource'
        i_action_them(step, 'count')
        self.assertEqual(step.context.stash, {'values': 3})



    def test_i_action_them_sum(self):
        step = MockedStep()
        with self.assertRaises(TerraformComplianceNotImplemented):
            i_action_them(step, 'something_else')

    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_i_expect_the_result_is_operator_than_number_more(self, *args):
        step = MockedStep()
        step.context.stash = {'values': 42}
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'more', 41))
        with self.assertRaises(Failure) as err:
            i_expect_the_result_is_operator_than_number(step, 'more', 43)
        self.assertTrue('42 is not more than 43' in str(err.exception))

    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_i_expect_the_result_is_operator_than_number_more_and_equal(self, *args):
        step = MockedStep()
        step.context.stash = {'values': 42}
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'more and equal', 42))
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'more and equal', 41))
        with self.assertRaises(Failure) as err:
            i_expect_the_result_is_operator_than_number(step, 'more and equal', 43)
        self.assertTrue('42 is not more and equal than 43' in str(err.exception))

    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_i_expect_the_result_is_operator_than_number_less(self, *args):
        step = MockedStep()
        step.context.stash = {'values': 42}
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'less', 43))
        with self.assertRaises(Failure) as err:
            i_expect_the_result_is_operator_than_number(step, 'less', 41)
        self.assertTrue('42 is not less than 41' in str(err.exception))

    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_i_expect_the_result_is_operator_than_number_less_and_equal(self, *args):
        step = MockedStep()
        step.context.stash = {'values': 42}
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'less and equal', 43))
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'less and equal', 42))
        with self.assertRaises(Failure) as err:
            i_expect_the_result_is_operator_than_number(step, 'less and equal', 41)
        self.assertTrue('42 is not less and equal than 41' in str(err.exception))

    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_i_expect_the_result_is_operator_than_number_equal(self, *args):
        step = MockedStep()
        step.context.stash = {'values': 42}
        self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'equal', 42))
        with self.assertRaises(Failure) as err:
            i_expect_the_result_is_operator_than_number(step, 'equal', 41)
        self.assertTrue('42 is not equal to 41' in str(err.exception))

    def test_i_expect_the_result_is_more_than_number_failure(self):
        step = MockedStep()
        step.context.stash = dict(values=3)
        with self.assertRaises(TerraformComplianceNotImplemented) as err:
            self.assertIsNone(i_expect_the_result_is_operator_than_number(step, 'invalid operator', 1))
        self.assertTrue('Invalid operator: invalid operator' in str(err.exception))

    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_it_fails(self, *args):
        step = MockedStep()
        step.context.type = 'some_type'
        step.context.name = 'some_name'
        with self.assertRaises(Failure):
            it_fails(step)

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_is_value_not_existent(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_is_value(step, 'something_else', 'some_value')
        self.assertEqual(step.state, 'skipped')

    def test_its_key_is_value_success(self):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_is_value(step, 'some_key', 'some_value')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_value')

    def test_its_key_is_value_exist_as_a_list(self):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value[0]',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_is_value(step, 'some_key', 'some_value')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_value[0]')

    def test_its_key_is_value_exist_in_values_int(self):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value[0]',
                'values': {
                    'storage_encrypted': 1
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': 2
                }
            }
        ]
        its_key_is_value(step, 'storage_encrypted', 1)
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_value[0]')

    def test_its_key_is_value_exist_in_values_bool(self):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value[0]',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_is_value(step, 'storage_encrypted', True)
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_value[0]')

    def test_its_key_is_value_dict_key_success(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_value(step, 'tags', 'tag_key_two')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_value')

    def test_its_key_is_value_dict_key_multi_success(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_value(step, 'tags', 'tag_key_one')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 2)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_value')
        self.assertEqual(step.context.stash[1]['some_key'], 'some_other_value')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_is_value_dict_key_failure(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_value(step, 'tags', 'tag_key_four')
        self.assertEqual(step.state, 'skipped')

    def test_its_key_is_value_dict_kv_success(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_value(step, 'tags', 'tag_key_two', 'tag_value_two')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_value')

    def test_its_key_is_value_dict_kv_success_2(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one_1',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one_2',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_value(step, 'tags', 'tag_key_one', 'tag_value_one_2')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_other_value')

    def test_its_key_is_value_dict_kv_multi_success(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_value(step, 'tags', 'tag_key_one', 'tag_value_one')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 2)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_value')
        self.assertEqual(step.context.stash[1]['some_key'], 'some_other_value')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_is_value_dict_kv_failure(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_value(step, 'tags', 'tag_key_four', 'whatever')
        self.assertEqual(step.state, 'skipped')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_is_value_dict_kv_failure_2(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_value(step, 'tags', 'tag_key_three', 'not_tag_key_three')
        self.assertEqual(step.state, 'skipped')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_metadata_has_something_key_non_existent(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_metadata_has_something(step, 'actions', 'create', has_step=True)
        self.assertEqual(step.state, 'skipped')
  

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_metadata_has_something_value_non_existent(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'actions': ['update'],
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_metadata_has_something(step, 'actions', 'create', has_step=True)
        self.assertEqual(step.state, 'skipped')        

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_metadata_has_something_success_string(self, *args):
        step = MockedStep()
        step.context.stash = [
            {   
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_metadata_has_something(step, 'some_key', 'some_value', has_step=True)
        self.assertNotEqual(step.state, 'skipped')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_value')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_metadata_has_something_success_bool(self, *args):
        step = MockedStep()
        step.context.stash = [
            {   
                'type': 'aws_db_instance',
                'some_key': True,
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_metadata_has_something(step, 'some_key', 'True', has_step=True)
        self.assertNotEqual(step.state, 'skipped')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertEqual(step.context.stash[0]['some_key'], True)

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_metadata_has_something_success_list(self, *args):
        step = MockedStep()
        step.context.stash = [
            {   
                'type': 'aws_db_instance',
                'some_key': ['some_value', 'some_other_value'],
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_metadata_has_something(step, 'some_key', 'some_value', has_step=True)
        self.assertNotEqual(step.state, 'skipped')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertEqual(step.context.stash[0]['some_key'][0], 'some_value')
        self.assertEqual(step.context.stash[0]['some_key'][1], 'some_other_value')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_metadata_has_something_int(self, *args):
        step = MockedStep()
        step.context.stash = [
            {   
                'type': 'aws_db_instance',
                'some_key': 1,
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_metadata_has_something(step, 'some_key', '1', has_step=True)
        self.assertNotEqual(step.state, 'skipped')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertEqual(step.context.stash[0]['some_key'], 1)

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_metadata_has_something_dictionary(self, *args):
        # special case, may be subject to change
        # check keys on dictionaries
        step = MockedStep()
        step.context.stash = [
            {   
                'type': 'aws_db_instance',
                'some_key': {'some_value': 'deeper_value'},
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_metadata_has_something(step, 'some_key', 'some_value', has_step=True)
        self.assertNotEqual(step.state, 'skipped')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertEqual(step.context.stash[0]['some_key']['some_value'], 'deeper_value')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_metadata_has_not_something_all_pairs_present(self, *args):
        step = MockedStep()
        step.context.stash = [
            {   
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_metadata_has_something(step, 'some_key', 'some_value', has_step=False)
        self.assertEqual(step.state, 'skipped')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_metadata_has_not_something_keys_non_existent(self, *args):
        step = MockedStep()
        step.context.stash = [
            {   
                'type': 'aws_db_instance',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_metadata_has_something(step, 'some_key', 'some_other_value', has_step=False)
        self.assertNotEqual(step.state, 'skipped')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertTrue('some_key' not in step.context.stash[0])

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_metadata_has_not_something_values_non_existent(self, *args):
        step = MockedStep()
        step.context.stash = [
            {   
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_metadata_has_something(step, 'some_key', 'some_other_value', has_step=False)
        self.assertNotEqual(step.state, 'skipped')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_value')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_find_keys_that_has_kv_structure(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'address': 'some_resource.id',
                'type': 'some_resource_type',
                'name': 'some_name',
                'values': [
                    {
                        'key': 'some_other_key',
                        'value': 'some_other_value'
                    },
                    {
                        'key': 'some_key',
                        'value': 'some_value'
                    }
                ]
            }
        ]
        step.context.type = 'resource'
        step.context.name = 'some_name'
        step.context.property_name = 'tags'
        step.context_sensitive_sentence = 'must'
        it_contains_something_old(step, 'some_key')
        self.assertEqual(step.context.stash[0]['values'], 'some_value')

    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_its_value_condition_match_the_search_regex_regex_null_value_is_parsed(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'address': 'some_resource.id',
                'type': 'some_resource_type',
                'name': 'some_name',
                'values': None
            }
        ]
        step.context.type = 'resource'
        step.context.name = 'some_name'
        step.context.property_name = 'tags'
        step.context_sensitive_sentence = 'must'

        with self.assertRaises(Failure):
            its_value_condition_match_the_search_regex_regex(step, 'must', 'something')
        with self.assertRaises(Failure):
            its_value_condition_equal(step, 'must', 'something')

    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_its_value_condition_match_the_search_regex_regex_success(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'address': 'some_resource.id',
                'type': 'some_resource_type',
                'name': 'some_name',
                'values': [
                    {
                        'key': 'some_other_key',
                        'value': 'some_other_value'
                    },
                    {
                        'key': 'some_key',
                        'value': 'some_value'
                    }
                ]
            }
        ]
        step.context.type = 'resource'
        step.context.name = 'some_name'
        step.context.property_name = 'tags'
        step.context_sensitive_sentence = 'must'

        self.assertEqual(its_value_condition_match_the_search_regex_regex(step, 'must', 'some_.*'), None)

        with self.assertRaises(Failure):
            self.assertEqual(its_value_condition_match_the_search_regex_regex(step, 'must not', 'some_.*'), None)
            self.assertEqual(its_value_condition_match_the_search_regex_regex(step, 'must not', 'some_other.*'), None)

    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_its_value_condition_equals(self, *args):
        step = MockedStep()
        expected_value = r"https://www.stackoverflow.com[as](.*)\s\t+$"
        step.context.stash = [
            {
                'address': 'some_resource.id',
                'type': 'some_resource_type',
                'name': 'some_name',
                'values': {
                    'some_key': expected_value
                }
            }
        ]
        step.context.type = 'resource'
        step.context.name = 'some_name'
        step.context.property_name = 'tags'
        step.context_sensitive_sentence = 'must'

        self.assertEqual(its_value_condition_equal(step, 'must', expected_value), None)
        self.assertEqual(its_value_condition_equal(step, 'must not', expected_value * 2), None)

        with self.assertRaises(Failure):
            self.assertEqual(its_value_condition_equal(step, 'must', expected_value + ' '), None)
            self.assertEqual(its_value_condition_equal(step, 'must not', expected_value), None)

    def test_its_key_is_not_value_exist_in_values_bool(self):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value[0]',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_is_not_value(step, 'storage_encrypted', True)
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_other_value')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_is_not_value_not_existent(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_is_not_value(step, 'something_else', 'some_value')
        self.assertEqual(step.state, 'skipped')

    def test_its_key_is_not_value_success(self):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_is_not_value(step, 'some_key', 'some_value')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_other_value')

    def test_its_key_is_not_value_exist_as_a_list(self):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value[0]',
                'values': {
                    'storage_encrypted': True
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value[0]',
                'values': {
                    'storage_encrypted': False
                }
            }
        ]
        its_key_is_not_value(step, 'some_key', 'some_value')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_other_value[0]')

    def test_its_key_is_not_value_exist_in_values_int(self):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value[0]',
                'values': {
                    'storage_encrypted': 1
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'storage_encrypted': 2
                }
            }
        ]
        its_key_is_not_value(step, 'storage_encrypted', 1)
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_other_value')

    def test_its_key_is_not_value_dict_key_success(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_not_value(step, 'tags', 'tag_key_two')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_other_value')

    def test_its_key_is_not_value_dict_key_case_success(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_ONE': 'tag_value_one',
                        'tag_key_TWO': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_ONE': 'tag_value_one',
                        'tag_key_THREE': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_not_value(step, 'tags', 'tag_key_TWO')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_other_value')

    def test_its_key_is_not_value_dict_key_multi_success(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_not_value(step, 'tags', 'tag_key_four')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 2)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_value')
        self.assertEqual(step.context.stash[1]['some_key'], 'some_other_value')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_is_not_value_dict_key_failure(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_not_value(step, 'tags', 'tag_key_one')
        self.assertEqual(step.state, 'skipped')

    def test_its_key_is_not_value_dict_kv_success(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_not_value(step, 'tags', 'tag_key_two', 'tag_value_two')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 1)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_other_value')

    def test_its_key_is_not_value_dict_kv_multi_success(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_not_value(step, 'tags', 'tag_key_two', 'tag_value_three')
        self.assertTrue(type(step.context.stash) is list)
        self.assertEqual(len(step.context.stash), 2)
        self.assertEqual(step.context.stash[0]['some_key'], 'some_value')
        self.assertEqual(step.context.stash[1]['some_key'], 'some_other_value')

    @patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld())
    def test_its_key_is_not_value_dict_kv_failure(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'type': 'aws_db_instance',
                'some_key': 'some_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_two': 'tag_value_two'
                    }
                }
            },
            {
                'type': 'aws_db_instance',
                'some_key': 'some_other_value',
                'values': {
                    'tags': {
                        'tag_key_one': 'tag_value_one',
                        'tag_key_three': 'tag_value_three'
                    }
                }
            }
        ]
        its_key_is_not_value(step, 'tags', 'tag_key_one', 'tag_value_one')
        self.assertEqual(step.state, 'skipped')

    @patch('terraform_compliance.common.error_handling.world', side_effect=MockedWorld())
    def test_its_value_condition_contain(self, *args):
        step = MockedStep()
        step.context.stash = [
            {
                'values': ['foo', 'bar']
            }
        ]
        step.context.property_name = 'some_thing'
        self.assertEqual({'values': ['foo', 'bar']},
                         its_value_condition_contain(step, 'must', 'foo'))
        self.assertEqual({'values': ['foo', 'bar']}, its_value_condition_contain(step, 'must not', 'baz'))
        with self.assertRaises(Failure):
            its_value_condition_contain(step, 'must', 'baz')
        with self.assertRaises(Failure):
            its_value_condition_contain(step, 'must not', 'foo')
