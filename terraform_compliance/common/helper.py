import re
from netaddr import IPNetwork


hcl_conditions = ["==", "!=", ">", "<", ">=", "<=", "&&", "||", "!"]


# A helper function that will be used to flatten a multi-dimensional multi-nested list
def flatten_list(input):
    new_list = []
    for i in input:
        if type(i) is list:
            i = flatten_list(i)
            for j in i:
                new_list.extend(j)
        else:
            new_list.extend(i)
    return new_list


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
        if check_if_cidr(ip_cidr) and check_if_cidr(ip_network):
            if IPNetwork(ip_cidr) in IPNetwork(ip_network):
                return True

    return False


# A helper function that compares port related data with given dictionary
def check_sg_rules(tf_conf, security_group, condition, proto, from_port, to_port, ports, cidr):

    if 'cidr_blocks' in security_group:
        if type(security_group['cidr_blocks']) is list:
            for i in range(0,len(security_group['cidr_blocks'])):
                if not check_if_cidr(security_group['cidr_blocks'][i]):
                    security_group['cidr_blocks'][i] = expand_variable(tf_conf,
                                                                       security_group['cidr_blocks'][i]
                                                                       ).get('default',
                                                                             security_group['cidr_blocks'][i])
        else:
            if not check_if_cidr(security_group['cidr_blocks']):
                security_group['cidr_blocks'] = expand_variable(tf_conf,
                                                                security_group['cidr_blocks']
                                                                ).get('default',
                                                                      security_group['cidr_blocks'])


    return validate_sg_rule(should_present=condition, proto=proto, from_port=from_port, to_port=to_port, ports=ports, cidr=cidr, params=assign_sg_params(security_group))


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
        raise AssertionError('Invalid configuration from_port can not be bigger than to_port. {} > {} {} in {}'.format(from_port,
                                                                                                                 to_port,
                                                                                                                 protocol,
                                                                                                                 cidr_blocks))

    return dict(protocol=protocol, from_port=from_port, to_port=to_port, cidr_blocks=cidr_blocks)


def validate_sg_rule(should_present, proto, from_port, to_port, ports, cidr, params):
    from_port = int(from_port)
    to_port = int(to_port)

    assert from_port <= to_port, 'Port range is defined incorrectly within the Scenario. ' \
                                 'Define it {}-{} instead of {}-{}.'.format(from_port,
                                                                            to_port,
                                                                            to_port,
                                                                            from_port)
    defined_range = set(range(params['from_port'], params['to_port']+1))

    if should_present:
        in_string = 'not in'
        given_range = set([int(port) for port in ports])
        intersection = not(given_range & defined_range)
        from_to_port = ','.join(ports)
    else:
        in_string = 'in'
        given_range = set(range(from_port, to_port+1))
        intersection = given_range & defined_range
        from_to_port = str(from_port) + '-' + str(to_port)

    if intersection and is_ip_in_cidr(cidr, params['cidr_blocks']):
        raise AssertionError("Port {}/{} {} {}/{} for {}".format(
                proto,
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
