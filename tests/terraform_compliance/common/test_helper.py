from unittest import TestCase
from terraform_compliance.common.helper import (
    flatten_list,
    check_if_cidr,
    is_ip_in_cidr,
    seek_key_in_dict,
    find_root_by_key,
    are_networks_same,
    convert_resource_type,
    seek_regex_key_in_dict_values,
    jsonify,
    remove_mounted_resources,
    get_resource_name_from_stash,
    dict_merge,
    is_list_of_dict,
    is_key_exist,
    transform_asg_style_tags,
    python_version_check,
    strip_iterations,
    get_most_child_module
)
from ddt import ddt, data, unpack

@ddt
class TestHelperFunctions(TestCase):

    def test_flatten_single_dimensional_list(self):
        a = ['a', 'b', 'c']
        b = ['a', 'b', 'c']

        self.assertEqual(flatten_list(a), b)

    def test_flatten_multi_dimensional_list(self):
        a = ['a', 'b', ['c']]
        b = ['a', 'b', 'c']

        self.assertEqual(flatten_list(a), b)

    def test_flatten_multi_dimensional_nested_list(self):
        a = ['a', 'b', ['c', ['d', 'e'], 'f'], 'g', 'h', 'i', ['j', 'k']]
        b = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']

        self.assertEqual(flatten_list(a), b)

    def test_check_if_cidr_success(self):
        self.assertTrue(check_if_cidr('10.0.0.0/8'))
        self.assertTrue(check_if_cidr('10.14.0.0/16'))
        self.assertTrue(check_if_cidr('10.0.0.0/24'))
        self.assertTrue(check_if_cidr('10.0.0.7/32'))

    def test_check_if_cidr_failure(self):
        self.assertFalse(check_if_cidr(123))
        self.assertFalse(check_if_cidr(False))
        self.assertFalse(check_if_cidr([]))
        self.assertFalse(check_if_cidr({}))

    def test_is_ip_in_cidr_success(self):
        self.assertTrue(is_ip_in_cidr('10.0.0.0/8', ['0.0.0.0/0']))
        self.assertTrue(is_ip_in_cidr('10.0.0.0/16', ['10.0.0.0/8']))
        self.assertTrue(is_ip_in_cidr('10.0.200.0/24', ['10.0.0.0/16']))
        self.assertTrue(is_ip_in_cidr('10.0.0.1/32', ['10.0.0.0/24']))

    def test_is_ip_in_cidr_failure(self):
        self.assertFalse(is_ip_in_cidr('200.0.0.0/16', ['10.0.0.0/8']))
        self.assertFalse(is_ip_in_cidr('10.200.0.0/24', ['10.0.0.0/16']))
        self.assertFalse(is_ip_in_cidr('10.0.1.1/32', ['10.0.0.0/24']))

    def test_seek_in_dict_finding_a_key_in_root(self):
        dictionary = dict(search_key=dict(something=[]))
        search_key = 'search_key'
        expected = [{'search_key': {'something': []}}]

        self.assertEqual(seek_key_in_dict(dictionary, search_key), expected)

    def test_seek_in_dict_finding_a_key_in_nested_dict(self):
        dictionary = dict(search_key=dict(something=dict(something_else=None)))
        search_key = 'something'
        expected = [{'something': {'something_else': None}}]

        self.assertEqual(seek_key_in_dict(dictionary, search_key), expected)

    def test_seek_in_dict_finding_multiple_keys_in_nested_dict(self):
        dictionary = dict(search_key=dict(something=dict(something_else=None, something=['something_else'])), something=[])
        search_key = 'something'
        expected = [{'something': {'something_else': None, 'something': ['something_else']}}, {'something': []}]

        self.assertEqual(seek_key_in_dict(dictionary, search_key), expected)

    def test_seek_in_dict_finding_values_in_non_dicts(self):
        dictionary = dict(search_key=dict(something=[]))
        search_key = 'something_else'
        expected = []

        self.assertEqual(seek_key_in_dict(dictionary, search_key), expected)

    def test_seek_in_dict_for_root_and_non_root_values(self):
        dictionary = dict(a=dict(b=dict(something=dict(test=[]))), something=["b"])
        search_key = "something"
        expected = [{'something':{'test': []}}, {'something':['b']}]

        self.assertEqual(seek_key_in_dict(dictionary, search_key), expected)

    def test_seek_in_dict_finding_values_in_non_dicts_on_root(self):
        dictionary = 'something_else'
        search_key = 'something_else'
        expected = []

        self.assertEqual(seek_key_in_dict(dictionary, search_key), expected)

    def test_find_root_by_key_single_return(self):
        haystack = dict(some_key=dict(values=dict(tags=[], something_else='something')))
        search_key = 'tags'
        expected = ['some_key']

        self.assertEqual(find_root_by_key(haystack, search_key), expected)

    def test_find_root_by_key_multiple_return(self):
        haystack = dict(some_key=dict(values=dict(tags=[], something_else='something')), other_key=dict(values=dict(tags=[], something_else='something')))
        search_key = 'tags'
        expected = ['other_key', 'some_key']

        self.assertEqual(sorted(find_root_by_key(haystack, search_key)), sorted(expected))

    def test_find_root_by_key_multiple_return_02(self):
        haystack = dict(some_key=dict(values=dict(tags=[], something_else='loki'), find_me='bingo'),
                        other_key=dict(values=dict(tags=[], something_else='thor'), find_me='b i n g o'))
        search_key = 'tags'
        return_key = 'find_me'
        expected = ['bingo', 'b i n g o']

        self.assertEqual(sorted(find_root_by_key(haystack, search_key, return_key)), sorted(expected))

    def test_are_networks_same_success(self):
        network_a = '192.168.0.0/24'
        networks = ['192.168.0.0/24']
        self.assertTrue(are_networks_same(network_a, networks))

    def test_are_networks_same_false(self):
        network_a = '192.168.0.0/24'
        networks = ['192.168.0.0/23']
        self.assertFalse(are_networks_same(network_a, networks))

    def test_convert_resource_type_success(self):
        self.assertEqual(convert_resource_type('AWS Security Group'), 'aws_security_group')

    def test_convert_resource_type_failure(self):
        self.assertEqual(convert_resource_type('test_resource'), 'test_resource')

    def test_seek_regex_in_dict_value_nested_dict(self):
        haystack = dict(search_key=dict(something='value'))
        key_name = 'something'
        needle = 'val.*'
        expected = ['value']

        self.assertEqual(seek_regex_key_in_dict_values(haystack, key_name, needle), expected)

    def test_jsonify(self):
        self.assertEqual(jsonify({}), {})
        self.assertEqual(jsonify([]), [])
        self.assertEqual(jsonify(12), 12)
        self.assertEqual(jsonify('something'), 'something')
        self.assertEqual(jsonify('{"test": "test_value"}'), {'test': 'test_value'})

    def test_remove_mounted_resources(self, *args):
        resource_list = {
            'address': 'aws_subnet.test',
            'type': 'aws_subnet',
            'name': 'test',
            'values': {
                'tags': None,
                'aws_vpc': [
                    {
                        'tags': {
                            'Environment': 'Sandbox',
                            'Name': 'mcrilly-sandbox'
                        },
                        'aws_subnet': [
                            {
                                'tags': None,
                                'terraform-compliance.mounted': True
                            }
                        ], 'terraform-compliance.mounted': True
                    }
                ]
            },
            'terraform-compliance.mounted_resources': {'key': 'aws_vpc'}
        }
        output = remove_mounted_resources([resource_list])
        self.assertEqual({'tags': None}, output[0]['values'])

    def test_get_resource_name_from_stash_address_exists(self):
        stash = {}
        self.assertEqual({'address': 'test'}, get_resource_name_from_stash(stash=stash, address='test'))

    def test_get_resource_name_from_stash(self):
        stash = [
            {
                'address': 'test'
            }
        ]
        self.assertEqual({'address': 'test'}, get_resource_name_from_stash(stash=stash))

    def test_dict_merge_no_change(self):
        source = {
                'a': [{'a': False}],
                'b': True
        }
        target ={
                'a': [{'a': True}]
        }
        self.assertEqual(dict_merge(source, target), source)

    def test_dict_merge_no_change_1(self):
        source = {
            'a': [{'a': False}],
            'b': True
        }
        target = []
        self.assertEqual(dict_merge(source, target), source)

    def test_dict_merge_no_change_2(self):
        self.assertEqual(dict_merge([], []), [])

    def test_dict_merge_success(self):
        source = {
            'a': [{'a': False}],
            'b': True
        }
        target ={
            'a': [{'b': 0}]
        }
        self.assertEqual(dict_merge(source, target), {'a': [{'a': False}, {'b': 0}], 'b': True})

    def test_is_list_of_dict_failures(self):
        self.assertFalse(is_list_of_dict(['a', 'b', 'c']))
        self.assertFalse(is_list_of_dict([1, 2, 3]))
        self.assertFalse(is_list_of_dict(['a', {'b':'c'}]))
        self.assertFalse(is_list_of_dict([False]))
        self.assertFalse(is_list_of_dict([]))

    def test_is_list_of_dict_successes(self):
        self.assertTrue(is_list_of_dict([{}]))
        self.assertTrue(is_list_of_dict([{'a:': [1]}]))
        self.assertTrue(is_list_of_dict([{'a:': 'b'}]))

    def test_is_key_exist_failures(self):
        self.assertFalse(is_key_exist('key', []))
        self.assertFalse(is_key_exist('key', [{}]))
        self.assertFalse(is_key_exist('key', [{'something': True}]))
        self.assertFalse(is_key_exist('key', [1, 2]))
        self.assertFalse(is_key_exist('key', ['key', 'b']))
        self.assertFalse(is_key_exist('key', [False]))
        self.assertFalse(is_key_exist('key', {'key': []}))

    def test_is_key_exist_successes(self):
        self.assertTrue(is_key_exist('key', [{'key': 'something'}]))
        self.assertTrue(is_key_exist('key', [{'something': True}, 2, 3, 4, {'key': True}]))
        self.assertTrue(is_key_exist('key', [{'something': True}, {'key': True}]))

    def test_transform_asg_style_tags_success(self):
        resource_list = {
            'address': 'aws_subnet.test',
            'type': 'aws_subnet',
            'name': 'test',
            'values': {
                'tags': None,
                'tag': [
                    {
                        'key': 'some_key',
                        'value': 'some_value'
                    }
                ],
            }
        }
        output = transform_asg_style_tags([resource_list])
        self.assertEqual(output[0]['values']['tags']['some_key'], 'some_value')

    def test_transform_asg_style_tags_return_directly(self):
        resource_list = 'abc'
        output = transform_asg_style_tags(resource_list)
        self.assertEqual(output, 'abc')

    def test_python_version_check_success(self):
        self.assertEqual(python_version_check(), 1)

    @data(['module.test["a"].aws_s3_bucket.test["a"]', 'module.test.aws_s3_bucket.test'],
          ['module.test[1].aws_s3_bucket.test["a"]','module.test.aws_s3_bucket.test'],
          ['module.test["a"].aws_s3_bucket.test[2]', 'module.test.aws_s3_bucket.test'],
          ['module.test["a-b"].aws_s3_bucket.test[2]', 'module.test.aws_s3_bucket.test'],
          ['module.test["a_B"].aws_s3_bucket.test[2]', 'module.test.aws_s3_bucket.test'],
          ['module.test["a_53917_xafad"].aws_s3_bucket.test[2]', 'module.test.aws_s3_bucket.test'],
          ['module.test["a_53917/xafad"].aws_s3_bucket.test[2]', 'module.test.aws_s3_bucket.test'],
          ['module.test["a_5391\\7/xafad"].aws_s3_bucket.test[2]', 'module.test.aws_s3_bucket.test'],
          ['module.test.aws_s3_bucket.test', 'module.test.aws_s3_bucket.test'])
    @unpack
    def test_strip_iterations_from_address(self, given, expected):
        self.assertEqual(strip_iterations(given), expected)

    @data(['module.a.module.b.module.c', 'c'],
          ['module.a', 'a'],
          ['module.a.module.b.aws_some_resource.c', 'b'],
          ['aws_some_resource.c', 'aws_some_resource.c'])
    @unpack
    def test_get_most_child_module(self, given, expected):
        self.assertEqual(get_most_child_module(given), expected)
