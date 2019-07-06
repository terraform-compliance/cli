import re
from netaddr import IPNetwork
from terraform_compliance.steps import resource_name
from terraform_compliance.common.exceptions import Failure
from collections.abc import Iterable
import json


class EmptyStash(object):
    pass


class Null(object):
    pass


def flatten_list(input):
    return list(flatten(input))


def flatten(items):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


def check_if_cidr( value ):
    regex = r'(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[0-9][0-9]|[0-9])\.(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[0-9][0-9]|[0-9])\.(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[0-9][0-9]|[0-9])\.(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[0-9][0-9]|[0-9])\/(3[0-2]|2[0-9]|1[0-9]|[0-9])'
    matches = re.match(regex, value)

    if matches is not None:
        return True

    return False


def is_ip_in_cidr(ip_cidr, cidr):
    for ip_network in cidr:
        if check_if_cidr(ip_cidr) and check_if_cidr(ip_network) and IPNetwork(ip_cidr) in IPNetwork(ip_network):
            return True

    return False


def are_networks_same(first_network, network_list):
    for second_network in network_list:
        if check_if_cidr(first_network) and check_if_cidr(second_network) and \
                IPNetwork(first_network) == IPNetwork(second_network):
            return True

    return False


# A helper function that compares port related data with given dictionary
def check_sg_rules(plan_data, security_group, condition):
    return validate_sg_rule(plan_data=assign_sg_params(plan_data),
                            params=security_group,
                            condition=condition)


def assign_sg_params(rule):
    from_port = int(rule.get('from_port', 0))
    to_port = int(rule.get('to_port', 0))

    protocol = [proto for proto in [rule.get('protocol', '-1')]]

    if protocol[0] == '-1' or type(protocol[0]) is int:
        protocol = ['tcp', 'udp']

    protocol[0] = protocol[0].lower()

    cidr_blocks = rule.get('cidr_blocks', [])

    if type(cidr_blocks) is not list:
        cidr_blocks = [cidr_blocks]

    if to_port == 0 and from_port == 0:
        to_port = 65535

    if from_port > to_port:
        raise Failure('Invalid configuration from_port can not be bigger than to_port. '
                                         '{} > {} {} in {}'.format(from_port,
                                                                   to_port,
                                                                   protocol,
                                                                   cidr_blocks))

    return dict(protocol=protocol, from_port=from_port, to_port=to_port, cidr_blocks=cidr_blocks)


def validate_sg_rule(plan_data, params, condition):
    from_port = int(params['from_port'])
    to_port = int(params['to_port'])

    assert from_port <= to_port, 'Port range is defined incorrectly within the Scenario. ' \
                                'Define it {}-{} instead of {}-{}.'.format(from_port,
                                                                           to_port,
                                                                           to_port,
                                                                           from_port)

    defined_range = set(range(plan_data['from_port'], plan_data['to_port']+1))
    defined_network_list = plan_data['cidr_blocks']
    given_network = params.get('cidr', None)

    # Condition: must only have
    # Fail only if ;
    # * the ports does not match and defined network is a subset of given network.
    if condition:
        given_range = set([int(port) for port in params['ports']])
        from_to_port = ','.join(params['ports'])

        # Set to True if ports are exactly same.
        port_intersection = given_range == defined_range

        # Set to True if one of the given networks is a subset.
        network_check = is_ip_in_cidr(given_network, defined_network_list)

        if not port_intersection and network_check:
            raise Failure('{}/{} ports are defined for {} network. '
                          'Must be limited to {}/{}'.format('/'.join(plan_data['protocol']),
                                                            '{}-{}'.format(plan_data['from_port'],
                                                                           plan_data['to_port']),
                                                            plan_data['cidr_blocks'],
                                                            '/'.join(plan_data['protocol']),
                                                            from_to_port))

    # Condition: must not have
    # Fail only if ;
    # * the ports match and networks match
    else:
        given_range = set(range(from_port, to_port+1))
        port_intersection = given_range & defined_range
        from_to_port = str(from_port) + '-' + str(to_port)
        network_intersection = is_ip_in_cidr(given_network, defined_network_list)

        if port_intersection and network_intersection:
            raise Failure('{}/{} ports are defined for {} network.'.format('/'.join(plan_data['protocol']),
                                                                           '{}-{}'.format(plan_data['from_port'],
                                                                                          plan_data['to_port']),
                                                                           plan_data['cidr_blocks']))

    return True


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
    if type(haystack) is dict:
        for key, value in haystack.items():
            if key.lower() == needle.lower():
                found.append({key: value})
            else:
                found.extend(seek_key_in_dict(value, needle))

    elif type(haystack) is list:
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
    :return: list of found keys & values
    '''
    regex = r'{}'.format(needle)
    found = list()
    if type(haystack) is dict:
        for key, value in haystack.items():
            if key.lower() == key_name.lower() or key_matched is not None:
                if type(value) is str:
                    matches = re.match(regex, value)

                    if matches is not None:
                        found.append(matches.group(0))
                    else:
                        found.extend(seek_regex_key_in_dict_values(value, key_name, needle, True))

                elif type(value) is dict:
                    found.extend(seek_regex_key_in_dict_values(value, key_name, needle, True))

                elif type(value) is list:
                    for value in haystack:
                        found.extend(seek_regex_key_in_dict_values(value, key_name, needle, True))

            else:
                found.extend(seek_regex_key_in_dict_values(value, key_name, needle, key_matched))

    elif type(haystack) is list:
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
    if type(haystack) is dict:
        for key, value in haystack.items():
            if not _depth:
                _inherited_key = key
                _return_value = key if not return_key else haystack[_inherited_key].get(return_key, _inherited_key)

            if key.lower() == needle.lower():
                found.append(_return_value)
            else:
                found.extend(find_root_by_key(value, needle, return_key, _inherited_key, _depth+1, _return_value))

    elif type(haystack) is list and _inherited_key is not None:
        for value in haystack:
            found.extend(find_root_by_key(value, needle, return_key, _inherited_key, _depth+1, _return_value))

    else:
        return []

    return list(set(found))


def jsonify(string):
    if type(string) is not str:
        return string

    try:
        return json.loads(string)
    except json.decoder.JSONDecodeError:
        return string


def get_resource_name_from_stash(stash, alternative_stash=None):
    if type(alternative_stash) is str or type(alternative_stash) is bool:
        if type(stash) is list:

            # Get the first number, since this is usually due to `count` usage in terraform
            if 'address' in stash[0]:
                return {'address': stash[0]['address'].replace('[0]','')}
            else:
                return {'address': stash[0]}

        else:
            if 'address' in alternative_stash:
                return alternative_stash
            else:
                return {'address': alternative_stash}
