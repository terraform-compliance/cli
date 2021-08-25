import re
from netaddr import IPNetwork
from terraform_compliance.steps import resource_name
from collections.abc import Iterable
from copy import deepcopy
import sys
from terraform_compliance.common.exceptions import TerraformComplianceInternalFailure
from semver import VersionInfo, compare
from terraform_compliance.common.defaults import Defaults
from radish.utils import console_write
try:
    import orjson as json
except ImportError:
    import json


class EmptyStash(object):
    pass


class Null(object):
    pass


class Match(object):
    def __init__(self, case_sensitive):
        self.case_sensitive = case_sensitive

    def equals(self, left, right):
        if not isinstance(left, (bool, int, float, str)) or not isinstance(right, (bool, int, float, str)):
            raise TypeError

        if self.case_sensitive:
            return str(left) == str(right)
        else:
            return str(left).lower() == str(right).lower()

    # gets something from a dictionary
    # needle == key
    def get(self, haystack, needle, default=None):
        if not isinstance(haystack, dict):
            return TypeError

        for key, value in haystack.items():
            if self.equals(key, needle):
                return value

        return default

    # checks if the collection (list, dict (key)) contains the element (only in first level, no seek)
    # needle should be a simple type
    # returns True for True in ['True']
    def contains(self, haystack, needle):
        if isinstance(haystack, (dict, list)):
            for key in haystack:
                if self.equals(key, needle):
                    return True
            return False

        raise TypeError

    # Assumes all incoming sets are sets of strings
    def issubset(self, set1, set2):
        if not isinstance(set1, Iterable) or isinstance(set1, str):
            raise TerraformComplianceInternalFailure('{} should be a non-str iterable'.format(set1))

        if not isinstance(set2, Iterable) or isinstance(set2, str):
            raise TerraformComplianceInternalFailure('{} should be a non-str iterable'.format(set2))

        if not self.case_sensitive:
            set1 = set(str(e).lower() for e in set1)
            set2 = set(str(e).lower() for e in set2)

        return set1 <= set2

    # re.match. overwrites the previous flag
    def regex_match(self, *args, **kwargs):
        regex_flag = 0 if self.case_sensitive else re.IGNORECASE
        return re.match(*args, **kwargs, flags=regex_flag)

    # seek key in dict but with case_sensitivity
    def seek_key_in_dict(self, haystack, needle):
        '''
        Searches needle in haystack ( could be dict, list, list of dicts, nested dicts, etc. ) and returns all findings
        as a list

        :param haystack: dict, list
        :param needle: search key
        :return: list of found keys & values
        '''
        found = list()
        if isinstance(haystack, dict):
            for key, value in haystack.items():
                if self.equals(key, needle):
                    found.append({key: value})
                else:
                    found.extend(self.seek_key_in_dict(value, needle))

        elif isinstance(haystack, list):
            for value in haystack:
                found.extend(self.seek_key_in_dict(value, needle))

        else:
            return []

        return found

    # ...
    # needle == value
    def seek_value_in_dict(self, needle, haystack, address=None):
        findings = []
        # if isinstance(haystack, (str, int, bool, float)) and str(needle) in str(haystack):  # this shouldn't be in but == instead
        #     findings.append(dict(values=needle, address=None))
        if isinstance(haystack, (str, int, bool, float)) and self.equals(needle, haystack):
            findings.append(dict(values=needle, address=None))

        elif isinstance(haystack, dict):
            address = haystack.get('address') if address is None else address

            for key, value in haystack.items():
                if isinstance(value, (dict, list)):
                    findings.extend(self.seek_value_in_dict(needle, value))

                elif isinstance(value, (str, bool, int, float)) and self.equals(needle, value):
                    findings.append(dict(values=needle, address=address))

        elif isinstance(haystack, list):
            # Check if this is a list of strings
            if all(isinstance(elem, str) for elem in haystack):
                findings.extend([elem for elem in haystack if self.equals(elem, needle)])

            # Otherwise, there are more stuff, so go recursive
            else:
                for value in haystack:
                    findings.extend(self.seek_value_in_dict(needle, value))

        return findings

    # ...
    # case sensitivity overwrites regex (if case insensitive, there is always re.IGNORECASE)
    # this's admittedly weird but convention/backwards compatibility...
    def seek_regex_key_in_dict_values(self, haystack, key_name, needle, key_matched=None):
        '''
        Searches needle in haystack ( could be dict, list, list of dicts, nested dicts, etc. ) and returns all findings
        as a list. The only difference from seek_key_in_dict is, we are assuming needle is in regex format here and we
        are searching for values instead.

        :param haystack: dict, list
        :param key_name: string of the key
        :param needle: regex search for the value
        :param key_matched: Internal use
        :return: list of found keys & values
        '''
        regex = r'^{}$'.format(needle)
        found = list()
        if isinstance(haystack, dict):
            for key, value in haystack.items():
                if isinstance(value, (bool, int, float)):
                    value = str(value)

                if self.equals(key, key_name) or key_matched is not None:
                    if isinstance(value, str):
                        matches = self.regex_match(regex, value)

                        if matches is not None:
                            found.append(matches.group(0))
                        else:
                            found.extend(self.seek_regex_key_in_dict_values(value, key_name, needle, True))

                    elif isinstance(value, dict):
                        found.extend(self.seek_regex_key_in_dict_values(value, key_name, needle, True))

                    elif isinstance(value, list):
                        for v in value:
                            found.extend(self.seek_regex_key_in_dict_values(v, key_name, needle, True))

                else:
                    found.extend(self.seek_regex_key_in_dict_values(value, key_name, needle, key_matched))

        elif isinstance(haystack, list):
            for value in haystack:
                found.extend(self.seek_regex_key_in_dict_values(value, key_name, needle, key_matched))

        else:
            return []

        return found


def flatten_list(input):
    return list(flatten(input))


def flatten(items):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


def check_if_cidr(value):
    try:
        re.compile(value)
        return True
    except TypeError as e:
        return False


def is_ip_in_cidr(ip_cidr, cidr):
    is_ip_regex = r'(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[0-9][0-9]|[0-9])' \
                  r'\.' \
                  r'(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[0-9][0-9]|[0-9])' \
                  r'\.' \
                  r'(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[0-9][0-9]|[0-9])' \
                  r'\.' \
                  r'(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[0-9][0-9]|[0-9])' \
                  r'\/' \
                  r'(3[0-2]|2[0-9]|1[0-9]|[0-9])'

    # IP is a not a regex string
    if re.match(is_ip_regex, ip_cidr) is not None:
        for ip_network in cidr:
            if check_if_cidr(ip_cidr) and check_if_cidr(ip_network) and IPNetwork(ip_cidr) in IPNetwork(ip_network):
                return True

        return False

    # IP is a possible regex string
    else:
        # The given regex is matching the CIDR within the plan
        for elem in cidr:
            if re.match(ip_cidr, elem) is None:
                return False
        return True


def are_networks_same(first_network, network_list):
    for second_network in network_list:
        if check_if_cidr(first_network) and check_if_cidr(second_network) and \
                IPNetwork(first_network) == IPNetwork(second_network):
            return True

    return False


def convert_resource_type(resource_type):
    '''
    Searchs given resource_type within resource_name array and returns the value if it is found

    :param resource_type: String of resource_type
    :return: converted or original resource_type
    '''
    if resource_type in resource_name.keys():
        resource_type = resource_name[resource_type]

    return resource_type


def seek_key_in_dict(haystack, needle):
    '''
    Searches needle in haystack ( could be dict, list, list of dicts, nested dicts, etc. ) and returns all findings
    as a list

    :param haystack: dict, list
    :param needle: search key
    :return: list of found keys & values
    '''
    found = list()
    if isinstance(haystack, dict):
        for key, value in haystack.items():
            if key.lower() == needle.lower():
                found.append({key: value})
            else:
                found.extend(seek_key_in_dict(value, needle))

    elif isinstance(haystack, list):
        for value in haystack:
            found.extend(seek_key_in_dict(value, needle))

    else:
        return []

    return found


def seek_regex_key_in_dict_values(haystack, key_name, needle, key_matched=None):
    '''
    Searches needle in haystack ( could be dict, list, list of dicts, nested dicts, etc. ) and returns all findings
    as a list. The only difference from seek_key_in_dict is, we are assuming needle is in regex format here and we
    are searching for values instead.

    :param haystack: dict, list
    :param key_name: string of the key
    :param needle: regex search for the value
    :param key_matched: Internal use
    :return: list of found keys & values
    '''
    regex = r'^{}$'.format(needle)
    found = list()
    if isinstance(haystack, dict):
        for key, value in haystack.items():
            if isinstance(value, (bool, int, float)):
                value = str(value)

            if key.lower() == key_name.lower() or key_matched is not None:
                if isinstance(value, str):
                    matches = re.match(regex, value, flags=re.IGNORECASE)

                    if matches is not None:
                        found.append(matches.group(0))
                    else:
                        found.extend(seek_regex_key_in_dict_values(value, key_name, needle, True))

                elif isinstance(value, dict):
                    found.extend(seek_regex_key_in_dict_values(value, key_name, needle, True))

                elif isinstance(value, list):
                    for v in value:
                        found.extend(seek_regex_key_in_dict_values(v, key_name, needle, True))

            else:
                found.extend(seek_regex_key_in_dict_values(value, key_name, needle, key_matched))

    elif isinstance(haystack, list):
        for value in haystack:
            found.extend(seek_regex_key_in_dict_values(value, key_name, needle, key_matched))

    else:
        return []

    return found


def find_root_by_key(haystack, needle, return_key=None, _inherited_key=None, _depth=0, _return_value=None):
    '''
    Searches needle in haystack ( could be dict, list, list of dicts, nested dicts, etc. ) and returns the root key
    that has this needle somewhere within it's children.

    :param haystack: dict, list
    :param needle: search key
    :param return_key: if this is given, then the result will be the root_key[return_key] instead of root_key
    :param _inherited_key: internal usage, do not pass this.
    :param _depth: internal usage, do not pass this.
    :param _return_value: internal usage, do not pass this.
    :return:
    '''
    found = list()
    if isinstance(haystack, dict):
        for key, value in haystack.items():
            if not _depth:
                _inherited_key = key
                _return_value = key if not return_key else haystack[_inherited_key].get(return_key, _inherited_key)

            if key.lower() == needle.lower():
                found.append(_return_value)
            else:
                found.extend(find_root_by_key(value, needle, return_key, _inherited_key, _depth + 1, _return_value))

    elif isinstance(haystack, list) and _inherited_key is not None:
        for value in haystack:
            found.extend(find_root_by_key(value, needle, return_key, _inherited_key, _depth + 1, _return_value))

    else:
        return []

    return list(set(found))


def jsonify(string):
    if not isinstance(string, str):
        return string

    try:
        return json.loads(string)
    except json.JSONDecodeError:
        return string


def recursive_jsonify(haystack):
    if isinstance(haystack, str):
        haystack = jsonify(haystack)
        if isinstance(haystack, (list, dict)):
            return recursive_jsonify(haystack)
        return haystack

    if isinstance(haystack, dict):
        haystack = {key: recursive_jsonify(value) for key, value in haystack.items()}

    if isinstance(haystack, list):
        haystack = [recursive_jsonify(value) for value in haystack]

    return haystack


def get_resource_name_from_stash(stash, alternative_stash=None, address=None):
    if address is not None:
        return {'address': address}

    if isinstance(alternative_stash, (str, bool)) or alternative_stash is None:
        if isinstance(stash, list):

            # Get the first number, since this is usually due to `count` usage in terraform
            if 'address' in stash[0] and stash[0]['address'] is not None:
                return {'address': stash[0]['address'].replace('[0]', '')}
            else:
                return {'address': stash[0]}

        else:
            if 'address' in alternative_stash:
                return alternative_stash
            else:
                return {'address': alternative_stash}


def get_resource_address_list_from_stash(resource_list):
    address_list = []
    for resource in resource_list:
        if 'address' in resource and resource['address'] not in address_list:
            address_list.append(resource['address'])

    return address_list


def remove_mounted_resources(resource_list):
    if not isinstance(resource_list, list):
        return resource_list

    resources = deepcopy(resource_list)
    for resource in resources:
        if 'terraform-compliance.mounted_resources' in resource:
            for key, mounted_resource_type in resource['terraform-compliance.mounted_resources'].items():
                if mounted_resource_type in resource['values']:
                    del resource['values'][mounted_resource_type]

    return resources


def search_regex_in_list(regex, target_list):
    if isinstance(target_list, list):
        return list(filter(re.compile(r'{}'.format(regex)).match, target_list))

    return False


def seek_value_in_dict(needle, haystack, address=None):
    findings = []
    if isinstance(haystack, (str, int, bool, float)) and str(needle) in str(haystack):
        findings.append(dict(values=needle, address=None))

    elif isinstance(haystack, dict):
        address = haystack.get('address') if address is None else address

        for key, value in haystack.items():
            if isinstance(value, (dict, list)):
                findings.extend(seek_value_in_dict(needle, value))
            elif isinstance(value, (str, bool, int, float)) and needle.lower() == str(value).lower():
                findings.append(dict(values=needle, address=address))

    elif isinstance(haystack, list):
        # Check if this is a list of strings
        if all(isinstance(elem, str) for elem in haystack):
            findings.extend([elem for elem in haystack if elem.lower() == needle.lower()])

        # Otherwise, there are more stuff, so go recursive
        else:
            for value in haystack:
                findings.extend(seek_value_in_dict(needle, value))

    return findings


def dict_merge(source, target):
    if not isinstance(source, dict) or not isinstance(target, dict):
        return source

    src = deepcopy(source)
    dst = deepcopy(target)
    for key, val in src.items():
        if key in dst and is_list_of_dict(val) and is_list_of_dict(dst[key]):
            for dst_elem in dst[key]:
                for each_key in dst_elem.keys():
                    if not is_key_exist(each_key, val):
                        src[key].append(dst_elem)

    return src


def is_list_of_dict(target_list):
    return isinstance(target_list, list) and len(target_list) and isinstance(target_list[0], dict)


def is_key_exist(key, target_list_of_dict):
    for each in target_list_of_dict:
        if isinstance(each, dict) and key in each.keys():
            return True

    return False


def transform_asg_style_tags(resource_list):
    if not isinstance(resource_list, list):
        return resource_list

    for resource in resource_list:
        tag = resource.get('values', {}).get('tag')

        if not resource.get('values', {}).get('tags'):
            resource['values']['tags'] = {}

        if tag:
            for elem in tag:
                if 'key' in elem and 'value' in elem:
                    resource['values']['tags'][elem['key']] = elem['value']

    return resource_list


def python_version_check():
    python_version = sys.version.split(' ')[0]

    if not python_version:
        raise TerraformComplianceInternalFailure('Could not determine python version. '
                                                 'Please post this to issues: '.format(sys.version))

    python_version = VersionInfo.parse(python_version)

    if compare(str(python_version), Defaults.supported_min_python_versions) < 0:
        console_write('ERROR: Python version {} is not supported. '
                      'You must have minimum {} version.'.format(python_version,
                                                                 Defaults.supported_min_python_versions[0]))
        sys.exit(1)

    return True

def merge_dicts(source, target):
    '''
    successor of dict_merge
    merges two dictionaries or lists into one
    overlapping list/dictionaries are also merged within each other

    assume target is low priority

    conflicts
        regular values: higher prio overrides
        dictionaries: merge conflicting dictionaries
        lists: higher prio overrides for regular values, merge any matching dictionary/list elements
            if len(target) > len(source):
                append the tail to the source


    # Confusing and less important comments:
    if isinstance(source, list) and isinstance(target, list):
        # shady, just extend?
        for i, v in enumerate(higher prio):
            if v is dict
                if lower has dict in the ith element
                    combine them
    if isinstance(source, dict) and isinstance(target, dict):
        if all elements are singular
            return {**target, **source}
        merged = {**target, **source} # source has priority over conflicts
        # find conflicting lists
        for all conflicting lists,
            # merged[key] = source[key] + target[key] # honestly depends on the situation
            merged[key] = merge_dicts(source[key], target[key])

        for all conflicting lists
            merged[key] = merge_dicts(source[key], target[key])
    decisions to make
        what happens to conflicting lists?
            should I drop one and keep the other (could be relevant on some cases)
            should I merge the lists? (could be relevant as well)

        what happens to conflicting dirs?
    if I have two lists
        lists have dictionaries in the same index
            merge those dictionaries

        # add remaining values of lower priority to higher priority
        ignore non dict values
    '''
    if isinstance(source, list) and isinstance(target, list):
        for i, value in enumerate(target):
            if i >= len(source):
                source.append(value)
            elif isinstance(value, dict) and isinstance(source[i], dict):
                merge_dicts(source[i], target[i])
            elif isinstance(value, list) and isinstance(source[i], list):
                merge_dicts(source[i], target[i])

    if isinstance(source, dict) and isinstance(target, dict):
        for key, value in target.items():
            if key not in source:
                source[key] = target[key]
            else:
                # regular values
                # do nothing
                # dictionaries
                if isinstance(value, dict) and isinstance(source[key], dict):
                    merge_dicts(source[key], target[key])
                elif isinstance(value, list) and isinstance(source[key], list):
                    merge_dicts(source[key], target[key])


def remove_constant_values(target):
    if isinstance(target, dict):
        for key, value in target.items():
            if isinstance(value, dict) and len(value) == 1 and 'constant_value' in value:
                target[key] = value['constant_value']
            elif isinstance(value, dict) or isinstance(value, list):
                remove_constant_values(value)
    elif isinstance(target, list):
        for value in target:
            remove_constant_values(value)


def strip_iterations(address):
    # Tried this with regex but it looks like the code was much less readable,
    # Hence trying to do it via quite a grunt way

    flag = False
    captured = ""
    capture_list = []
    capture_start = "["
    capture_end = "]"

    for letter in address:
        if letter == capture_start:
            flag = True
            captured = ""
        elif letter == capture_end:
            flag = False
            capture_list.append('{}{}'.format(captured, capture_end))

        if flag:
            captured += letter

    for replacement in capture_list:
        address = address.replace(replacement, '')

    return address


def get_most_child_module(module):
    modules = module.split('.')
    current_module = None
    for i in range(0, len(modules)):
        if modules[i] == 'module':
            current_module = modules[i+1]

    if not current_module:
        return module

    return current_module

