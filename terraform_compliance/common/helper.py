import re
from netaddr import IPNetwork


# A helper function that will be used to flattan a multi-dimensional multi-nested list
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


def is_ip_in_cidr( ip_cidr, cidr ):
    return_value = False
    cidr = eval(cidr)
    if type(cidr) is list:
        for ip_network in cidr:
            if IPNetwork(ip_cidr) in IPNetwork(ip_network):
                return_value = True
    else:
        if IPNetwork(ip_cidr) in IPNetwork(cidr):
            return_value = True

    return return_value


# A helper function that compares port related data with given dictionary
def check_sg_rules(tf_conf, security_group, proto, port, cidr):

    if 'cidr_blocks' in security_group:
        if type(security_group['cidr_blocks']) is list:
            for i in range(0,len(security_group['cidr_blocks'])):
                if not check_if_cidr(security_group['cidr_blocks'][i]):
                    security_group['cidr_blocks'][i] = expand_variable(tf_conf, security_group['cidr_blocks'][i])['default']
        else:
            if not check_if_cidr(security_group['cidr_blocks']):
                security_group['cidr_blocks'] = expand_variable(tf_conf, security_group['cidr_blocks'])['default']


    validate_sg_rule(proto=proto, port=port, cidr=cidr, params=assign_sg_params(security_group))

def assign_sg_params(rule):
    protocol = ''
    from_port = 0
    to_port = 0
    cidr_blocks = None

    for y in rule:
        if y == 'protocol':
            protocol = [rule[y]]
            if protocol[0] == '-1':
                protocol = ['tcp', 'udp']

        if y == 'from_port' and rule[y] > 0:
            from_port = rule[y]

        if y == 'to_port' and rule[y] > 0:
            to_port = rule[y]

        if y == 'cidr_blocks' and type(rule[y] is list):
            cidr_blocks = rule[y]

    if to_port == 0 and from_port == 0:
        to_port = 65535

    return dict(protocol=protocol, from_port=int(from_port), to_port=int(to_port), cidr_blocks=str(cidr_blocks))


def validate_sg_rule(proto, port, cidr, params):
    if (params['to_port'] > params['from_port'] and params['from_port'] <= port <= params['to_port'] and proto in params['protocol'] and is_ip_in_cidr(cidr, params['cidr_blocks'])) or \
       (params['from_port'] > params['to_port'] and params['to_port'] <= port <= params['from_port'] or proto in params['protocol'] and is_ip_in_cidr(cidr, params['cidr_blocks'])) or \
       (params['from_port'] == params['to_port'] and params['from_port'] == port and proto in params['protocol'] and is_ip_in_cidr(cidr, params['cidr_blocks'])):
        return True

    raise AssertionError('Found {}/{} in {}/{}-{} for {}'.format(proto, port, params['protocol'], params['from_port'], params['to_port'], params['cidr_blocks']))


def change_value_in_dict(target_dictionary, path_to_change, value_to_change):
    if type(path_to_change) is str:
        path_to_change = path_to_change.split('.')

    if type(path_to_change) is not list:
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
