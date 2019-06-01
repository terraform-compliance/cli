import re
from netaddr import IPNetwork
from terraform_compliance.steps import resource_name
from terraform_compliance.common.exceptions import Failure
from collections.abc import Iterable


def flatten_list(input):
    return list(flatten(input))


def flatten(items):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


def generate_target_resource( target_string ):
    target = target_string.strip()
    target = 'resource.{}'.format(target).split('.')

    if target[-1] in ['id', 'name']:
        target.pop(-1)

    return target


def expand_variable(tf_conf, value):
    regex = r'\${var.(.*)\}'
    matches = re.match(regex, value)

    if matches is None:
        if 'module' in value:
            return 'None'

        return value

    if matches.group(1) not in tf_conf['variable']:
        return value

    return tf_conf['variable'][matches.group(1)]


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


# A helper function that compares port related data with given dictionary
def check_sg_rules(security_group, condition, plan_data):
    return validate_sg_rule(should_present=condition,
                            plan_data=plan_data,
                            params=assign_sg_params(security_group))


def assign_sg_params(rule):
    from_port = int(rule.get('from_port', 0))
    to_port = int(rule.get('to_port', 0))

    protocol = [proto for proto in [rule.get('protocol', '-1')]]

    # TODO: Make IANA Protocol numbers matching here.
    # http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
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


def validate_sg_rule(should_present, plan_data, params):
    from_port = int(plan_data['from_port'])
    to_port = int(plan_data['from_port'])

    assert from_port <= to_port, 'Port range is defined incorrectly within the Scenario. ' \
                                 'Define it {}-{} instead of {}-{}.'.format(from_port,
                                                                            to_port,
                                                                            to_port,
                                                                            from_port)
    defined_range = set(range(params['from_port'], params['to_port']+1))

    if should_present:
        in_string = 'not in'
        given_range = set([int(port) for port in plan_data['ports']])
        intersection = not(given_range & defined_range)
        from_to_port = ','.join(plan_data['ports'])
    else:
        in_string = 'in'
        given_range = set(range(from_port, to_port+1))
        intersection = given_range & defined_range
        from_to_port = str(from_port) + '-' + str(to_port)

    if intersection and is_ip_in_cidr(plan_data.get('cidr', None), params['cidr_blocks']):
        raise Failure("Port {}/{} {} {}/{} for {}".format(
                plan_data['proto'],
                '{}-{}'.format(params['from_port'], params['to_port']),
                in_string,
                '/'.join(params['protocol']),
                from_to_port,
                params['cidr_blocks']))

    return True

def change_value_in_dict(target_dictionary, path_to_change, value_to_change):
    if type(path_to_change) is str:
        path_to_change = path_to_change.split('.')

    if type(path_to_change) is not list:
        return False

    for x in range(0,len(path_to_change)):
        for condition in hcl_conditions:
            if condition in path_to_change[x]:
                return False

    path_to_adjust = '["{}"]'.format('"]["'.join(path_to_change))

    try:
        target = eval('target_dictionary{}'.format(path_to_adjust))

        for key, value in value_to_change.items():
            if 'type' in value:
                type_key = value['type']
                source = value
                source['referenced_name'] = key

                if type_key not in target:
                    target[type_key] = list()
                elif type_key in target and type(target[type_key]) is not list:
                        target[type_key] = [target[type_key]]

                target[type_key].append(source)

        target.update(value_to_change)

        try:
            exec('target_dictionary{}.update({})'.format(path_to_adjust, target))
        except:
            # Yes I know, this is against PEP8.
            pass

    except KeyError:
        pass


def strip_conditions(string):
    for condition in hcl_conditions:
        string = string.replace(condition, "")


    string = string.split(" ")

    return string[0]


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


def find_root_by_key(haystack, needle, return_key=None, inherited_key=None, depth=0, return_value=None):
    found = list()
    if type(haystack) is dict:
        for key, value in haystack.items():
            if not depth:
                inherited_key = key
                return_value = key if not return_key else haystack[inherited_key].get(return_key, inherited_key)

            if key.lower() == needle.lower():
                found.append(return_value)
            else:
                found.extend(find_root_by_key(value, needle, return_key, inherited_key, depth+1, return_value))

    elif type(haystack) is list and inherited_key is not None:
        for value in haystack:
            found.extend(find_root_by_key(value, needle, return_key, inherited_key, depth+1, return_value))

    else:
        return []

    return list(set(found))
