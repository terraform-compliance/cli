from terraform_compliance.common.helper import (
    check_if_cidr,
    is_ip_in_cidr
)
from terraform_compliance.common.exceptions import (
    TerraformComplianceInvalidData,
    TerraformComplianceInternalFailure
)


class SecurityGroupRule(object):
    def __init__(self, **kwargs):
        self.from_port = kwargs.get('from_port', kwargs.get('values', {}).get('from_port'))
        self.to_port = kwargs.get('to_port', kwargs.get('values', {}).get('to_port'))
        self.ports = str(kwargs.get('port'))
        self.protocol = [proto for proto in [kwargs.get('protocol', kwargs.get('values', {}).get('protocol', '-1'))]]
        self.cidr_blocks = kwargs.get('cidr_blocks', kwargs.get('values', {}).get('cidr_blocks', []))
        self.address = kwargs.get('values', {}).get('address')
        self.description = kwargs.get('description', kwargs.get('values', {}). get('description'))
        self.port_is_single = False

        self._normalise_protocols()
        self._normalise_ports()
        self._check_for_invalidations()

    def _normalise_ports(self):
        self.from_port = 0 if self.ports == 'any' else self.from_port
        self.to_port = 0 if self.ports == 'any' else self.to_port

        # Sometimes terraform reports ports like this
        if self.from_port == 0 and self.to_port == 0:
            self.to_port = 65535
            self.port_is_single = False

        if not self.from_port and not self.to_port:

            # There is no port information, so we need to set everything to ALL, because
            # terraform does that automatically.
            if self.ports == 'None':
                self.from_port = 1
                self.to_port = 65535
            else:
                self._expand_ports(self.ports)

        else:
            self.from_port = int(self.from_port)
            self.to_port = int(self.to_port)

            self.from_port = self.from_port if self.from_port > 0 else 1
            self.to_port = self.to_port if self.to_port > 0 else 1
            self.ports = self._get_port_range(self.from_port, self.to_port)

            self.port_is_single = True if self.from_port == self.to_port else False

    def _normalise_protocols(self):
        # TODO: Implement other protocols, not just TCP and UDP.
        # There is always one protocol in the list as an input.
        if self.protocol[0] == '-1' or isinstance(self.protocol[0], int) or self.protocol[0] == 'any':
            self.protocol = ['tcp', 'udp', 'icmp']
        else:
            self.protocol[0] = self.protocol[0].lower()

    def _check_for_invalidations(self):
        if (self.from_port and self.to_port) and self.from_port > self.to_port and ('tcp' in self.protocol or 'udp' in self.protocol):
            raise TerraformComplianceInvalidData('Invalid configuration from_port can not be bigger than to_port. '
                                                 '{} > {} {} in {}'.format(self.from_port,
                                                                           self.to_port,
                                                                           self.protocol,
                                                                           self.cidr_blocks))

        if self.cidr_blocks is None:
            raise TerraformComplianceInvalidData('A cidr range must be given.')

        if isinstance(self.cidr_blocks, list):
            for cidr in self.cidr_blocks:
                if check_if_cidr(cidr) is False:
                    raise TerraformComplianceInvalidData('{} is not a valid CIDR.'.format(cidr))
        elif isinstance(self.cidr_blocks, str):
            if check_if_cidr(self.cidr_blocks) is False:
                raise TerraformComplianceInvalidData('{} is not a valid CIDR.'.format(self.cidr_blocks))
        else:
            raise TerraformComplianceInvalidData('Invalid CIDR Type {} : {}'.format(type(self.cidr_blocks),
                                                                                    self.cidr_blocks))

        if not self.protocol:
            raise TerraformComplianceInvalidData('A protocol must be given.')

    def _expand_ports(self, port):
        if '-' in port:
            self.from_port, self.to_port = [int(port_number) for port_number in port.split('-')]
            self.from_port = self.from_port if self.from_port > 0 else 1
            self.to_port = self.to_port if self.to_port > 0 else 1
            self.ports = self._get_port_range(self.from_port, self.to_port)
            self.port_is_single = False

        elif ',' in port:
            self.from_port = None
            self.to_port = None
            self.port_is_single = False
            self.ports = set([int(port_number) for port_number in port.split(',') if int(port_number) > 0])

        elif port.isnumeric():
            self.from_port = self.to_port = int(port)
            self.ports = self._get_port_range(self.from_port, self.to_port)
            self.port_is_single = True

        else:
            raise TerraformComplianceInternalFailure('Unexpected situation. '
                                                     'Please report this port structure: {}'.format(vars(self)))

    @staticmethod
    def _get_port_range(from_port, to_port):
        if to_port >= from_port:
            return set(range(from_port, to_port+1))
        else:
            return set(range(to_port, from_port+1))


class SecurityGroup(object):
    def __init__(self, given_reqs, security_groups_in_plan, address='test_sg'):
        self.given = given_reqs
        self.sgs = self._clean(security_groups_in_plan)
        self.sgs = [self.sgs] if isinstance(self.sgs, dict) else self.sgs
        self.address = address

        self.exact_match = False
        self.negative_match = True
        self.include_match = False
        self.singular_check = True
        self.multiple_check = False

        self.given_rule = SecurityGroupRule(**given_reqs)
        self.plan_rules = [SecurityGroupRule(**rule_data) for rule_data in self.sgs if rule_data.get('cidr_blocks')]

        self.found_ports = set()

    def must_only_have(self):
        self.exact_match = True
        self.negative_match = False
        self.include_match = False
        self.singular_check = False

    # This is the default for validate() method
    def must_not_have(self):
        self.exact_match = False
        self.negative_match = True
        self.include_match = False
        self.singular_check = True

    def must_have(self):
        self.exact_match = False
        self.negative_match = False
        self.include_match = True
        self.singular_check = False

    def validate(self):

        #
        # Make it flexible enough to support other scenarios
        # Currently we have ;
        #
        # 1. "must only" ports, which means all ports defined in ALL security group rules must have exactly the same
        #    ports.
        # 2. "must not" ports, which means the ports defined in ANY security group, should not have this port with cidr
        #    , etc.
        # 3. "must have" ports, which means, the ports defined in ALL security groups should include these ports. < This
        #    doesn't exist yet.
        #

        ports_found = set()
        for rule in self.plan_rules:
            # General Controls that is applicable for every scenario
            network_check = self._validate_network(rule.cidr_blocks)
            ports_check = self._validate_ports(rule)
            protocol_check = self._validate_protocol(rule)

            # Apply enforcement on every rule. Only applicable for 'must not have'
            if self.singular_check:
                result, error = self._run_singular_validation(rule, network_check, ports_check, protocol_check)
                if result is False:
                    return result, error

            # Apply enforcement after the for loop, gather information first.
            elif not self.singular_check and network_check and protocol_check:
                # Gather all ports defined within the Security Group rule that matches CIDR.
                ports_found = ports_found | rule.ports

        # Finalise singular checks as returning True if nothing happens,
        # since it must have failed already.
        if self.singular_check:
            return True, None

        # Process non singular checks
        else:
            # So if the scenario is 'must only have'
            # Then sets must be exactly equal to each other.
            # If not, first get GIVEN->FOUND, FOUND->GIVEN and no disjoint differences
            # then return an error output
            errors = []
            if self.exact_match:
                if ports_found == self.given_rule.ports:
                    return True, None

                # Create errors
                given_found_diff = self.given_rule.ports - ports_found
                found_given_diff = ports_found - self.given_rule.ports
                nodisjoint = self.given_rule.ports.isdisjoint(ports_found)

                if given_found_diff:
                    e = self._prepare_output(given_found_diff)
                    errors.append('{}/{} port{} not defined within {} network{} in {}.'.format(e['protocol'],
                                                                                               e['ports'],
                                                                                               e['ports_plural'],
                                                                                               e['cidr_blocks'],
                                                                                               e['cidr_blocks_plural'],
                                                                                               e['address']))

                if found_given_diff:
                    e = self._prepare_output(found_given_diff)
                    errors.append('{}/{} port{} defined within {} network{} in {}.'.format(e['protocol'],
                                                                                           e['ports'],
                                                                                           e['ports_plural'],
                                                                                           e['cidr_blocks'],
                                                                                           e['cidr_blocks_plural'],
                                                                                           e['address']))

                if nodisjoint:
                    e = self._prepare_output(set())
                    errors.append('None of the ports given defined within {} network{} in '
                                  '{}.'.format(e['cidr_blocks'],
                                               e['cidr_blocks_plural'],
                                               e['address']))

            # If the scenario is 'must have', then given ports must be a subset (or equal) of ports_found
            # If not, found which ports are missing via GIVEN->FOUND diff
            else:
                if self.given_rule.ports <= ports_found:
                    return True, None

                given_found_diff = self.given_rule.ports - ports_found

                if given_found_diff:
                    e = self._prepare_output(given_found_diff)
                    errors.append('{}/{} port{} not defined within {} network{} in {}.'.format(e['protocol'],
                                                                                               e['ports'],
                                                                                               e['ports_plural'],
                                                                                               e['cidr_blocks'],
                                                                                               e['cidr_blocks_plural'],
                                                                                               e['address']))
            if errors:
                return False, '{}'.format("\n".join(errors))

    def _run_singular_validation(self, rule, network_check, ports_check, protocol_check):
        if self.negative_match and network_check and ports_check and protocol_check:
            e = self._prepare_output(rule, ports_check, protocol_check)
            return False, '{}/{} port{} defined within {} network{} in {}.'.format(e['protocol'],
                                                                                   e['ports'],
                                                                                   e['ports_plural'],
                                                                                   e['cidr_blocks'],
                                                                                   e['cidr_blocks_plural'],
                                                                                   e['address'])
        else:
            return True, None

    def _validate_network(self, cidr_in_plan):
        return is_ip_in_cidr(self.given_rule.cidr_blocks, cidr_in_plan)

    def _validate_ports(self, rule_data):
        return self.given_rule.ports & rule_data.ports

    def _validate_protocol(self, rule_data):
        return set(self.given_rule.protocol) & set(rule_data.protocol)

    def _prepare_output(self, rule, ports_check=None, protocol_check=None):
        output = dict()

        if self.singular_check:
            output['protocol'] = str(list(protocol_check)[0]) if len(protocol_check) == 1 else '({})'.format(','.join(str(s) for s in protocol_check))
            output['cidr_blocks'] = rule.cidr_blocks[0] if len(rule.cidr_blocks) == 1 else ', '.join(rule.cidr_blocks)
            output['cidr_blocks_plural'] = '' if len(rule.cidr_blocks) == 1 else 's'
            output['address'] = rule.address if rule.address else self.address
            output['ports'] = str(list(ports_check)[0]) if len(ports_check) == 1 else '({})'.format(','.join(str(s) for s in ports_check))
            # TODO: If the ports output is too large, make it smaller by showing a range only.
            output['ports_plural'] = ' is' if len(ports_check) == 1 else 's are'
        else:
            output['protocol'] = str(list(self.given_rule.protocol)[0]) if len(self.given_rule.protocol) == 1 else '({})'.format(','.join(str(s) for s in self.given_rule.protocol))
            output['cidr_blocks'] = self.given_rule.cidr_blocks
            output['cidr_blocks_plural'] = ''
            output['address'] = self.address
            output['ports'] = str(list(rule)[0]) if len(rule) == 1 else '({})'.format(','.join(str(s) for s in rule))
            # TODO: If the ports output is too large, make it smaller by showing a range only.
            output['ports_plural'] = ' is' if len(rule) == 1 else 's are'

        return output

    def _clean(self, sg_array):
        if isinstance(sg_array, list):
            for sg in sg_array:
                self._clean(sg)

        elif isinstance(sg_array, dict):
            if 'self' in sg_array:
                sg_array.pop('self')

        return sg_array


def convert_single_rule_to_a_sg(rule_obj):
    if not rule_obj.get('values'):
        return False

    return {
        'address': '{}'.format(rule_obj.get('address')),
        'mode': 'managed',
        'type': 'aws_security_group',
        'name': '{}'.format(rule_obj.get('address')),
        'provider_name': rule_obj.get('provider_name'),
        'values': {
            'description': rule_obj['values'].get('decription'),
            'name': '{}'.format(rule_obj.get('address')),
            rule_obj['values']['type']: [
                {
                    'cidr_blocks': rule_obj['values']['cidr_blocks'],
                    'description': rule_obj['values']['description'],
                    'from_port': rule_obj['values']['from_port'],
                    'ipv6_cidr_blocks': rule_obj['values']['ipv6_cidr_blocks'],
                    'prefix_list_ids': rule_obj['values']['prefix_list_ids'],
                    'protocol': rule_obj['values']['protocol'],
                    'self': rule_obj['values']['self'],
                    'to_port': rule_obj['values']['to_port'],
                    'type': rule_obj['values']['type']
                }
            ]
        }
    }
