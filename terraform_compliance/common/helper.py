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
def check_port_cidr_ranges(tf_conf, security_group, proto, port, cidr):
    protocol = ''
    from_port = 0
    to_port = 0
    cidr_blocks = None
    giveError = False

    # This is because of resource_mounting
    #if 'referenced_name' in security_group:
    #    return

    if 'cidr_blocks' in security_group:
        if type(security_group['cidr_blocks']) is list:
            for i in range(0,len(security_group['cidr_blocks'])):
                if not check_if_cidr(security_group['cidr_blocks'][i]):
                    security_group['cidr_blocks'][i] = expand_variable(tf_conf, security_group['cidr_blocks'][i])['default']
        else:
            if not check_if_cidr(security_group['cidr_blocks']):
                security_group['cidr_blocks'] = expand_variable(tf_conf, security_group['cidr_blocks'])['default']

    #TODO: Add custom protocol support where HCL has numbers instead of protocol names like tcp, udp
    #TODO: Add IP Range/Netmask check with the given CIDR.
    for y in security_group:
        if security_group[y] == proto:
            protocol = security_group[y]

        if y == 'from_port' and security_group[y] > 0:
            from_port = int(security_group[y])

        if y == 'to_port' and security_group[y] > 0:
            to_port = int(security_group[y])

        if y == 'cidr_blocks':
            if type(security_group[y] is list):
                cidr_blocks = str(security_group[y])

    if int(to_port) > int(from_port):
        if int(from_port) <= port <= int(to_port) and protocol == proto and is_ip_in_cidr(cidr, cidr_blocks):
            giveError = True
    elif int(from_port) > int(to_port):
        if int(to_port) <= port <= int(from_port) or protocol == proto and is_ip_in_cidr(cidr, cidr_blocks):
            giveError = True
    elif int(from_port) == int(to_port):
        if int(from_port) == port and protocol == proto and is_ip_in_cidr(cidr, cidr_blocks):
            giveError = True

    if giveError:
        raise AssertionError('Found {}/{} in {}/{}-{} for {}'.format(proto, port, protocol, from_port,
                                                                     to_port, cidr_blocks))


def change_value_in_dict(target_dictionary, path_to_change, value_to_change):
    if type(path_to_change) is str:
        path_to_change = path_to_change.split('.')

    if type(path_to_change) is not list:
        return False

    path_to_adjust = '["{}"]'.format('"]["'.join(path_to_change))
    path_to_check  = '["{}"]["type"]'.format('"]["'.join(path_to_change))
    path_to_add    = '["{}"]'.format('"]["'.join(path_to_change[:-1]))


    try:
        target = eval('target_dictionary{}'.format(path_to_adjust))

        for key, value in value_to_change.items():
            if 'type' in value:
                type_key = value['type']
                source = value
                source['referenced_name'] = key

                if type_key not in target:
                    target[type_key] = list()
                elif type_key in target:
                    if type(target[type_key]) is not list:
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
