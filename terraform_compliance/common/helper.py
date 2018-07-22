


# A helper function that will be used to flattan a multi-dimensional multi-nested list
def flatten_list(input):
    print '<=== {}'.format(input)
    new_list = []
    for i in input:
        if type(i) is list:
            i = flatten_list(i)
            for j in i:
                new_list.extend(j)
        else:
            new_list.extend(i)
    print '===> {}'.format(new_list)
    return new_list


# A helper function that compares port related data with given dictionary
def check_port_cidr_ranges(security_group, proto, port, cidr):
    protocol = ''
    from_port = 0
    to_port = 0
    cidr_blocks = False
    giveError = False

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
                # There must be a CIDR check here.
                # if cidr(parameter) is a member of given CIDR blocks,
                # then accept it.
                cidr_blocks = str(security_group[y][0])
            else:
                cidr_blocks = str(security_group[y])

    if int(to_port) > int(from_port):
        if int(from_port) <= port <= int(to_port) and protocol == proto and cidr_blocks == cidr:
            giveError = True
    elif int(from_port) > int(to_port):
        if int(to_port) <= port <= int(from_port) or protocol == proto and cidr_blocks == cidr:
            giveError = True
    elif int(from_port) == int(to_port):
        if int(from_port) == port and protocol == proto and cidr_blocks == cidr:
            giveError = True

    if giveError:
        raise AssertionError("Found " + proto + "/" + str(port) + " for " + str(cidr_blocks))