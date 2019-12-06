from terraform_compliance.common.helper import (
    check_if_cidr,
    is_ip_in_cidr
)
from terraform_compliance.common.exceptions import (
    Failure,
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
        self.port_is_list = False

        self._normalise_ports()
        self._check_for_invalidations()

    def _normalise_ports(self):
        # TODO: Implement other protocols, not just TCP and UDP.
        if self.protocol[0] == '-1' or type(self.protocol[0]) is int:
            self.protocol = ['tcp', 'udp']
        else:
            self.protocol[0] = self.protocol[0].lower()

        if self.from_port == 0 and self.to_port == 0:
            self.to_port = 65535

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

    def _check_for_invalidations(self):
        if self.from_port > self.to_port:
            raise TerraformComplianceInvalidData('Invalid configuration from_port can not be bigger than to_port. '
                                                 '{} > {} {} in {}'.format(self.from_port,
                                                                           self.to_port,
                                                                           self.protocol,
                                                                           self.cidr_blocks))

        if self.cidr_blocks is None:
            raise TerraformComplianceInvalidData('A cidr range must be given.')

        for cidr in self.cidr_blocks:
            if check_if_cidr(cidr) is False:
                raise TerraformComplianceInvalidData('{} is not a valid CIDR.'.format(cidr))

        if not self.protocol:
            raise TerraformComplianceInvalidData('A protocol must be given.')

    def _expand_ports(self, port):
        if '-' in port:
            self.from_port, self.to_port = port.split('-')
            self.from_port = self.from_port if self.from_port > 0 else 1
            self.to_port = self.to_port if self.to_port > 0 else 1
            self.ports = set(range(self.from_port, self.to_port))
            self.port_is_list = True

        elif ',' in port:
            self.from_port = None
            self.to_port = None
            self.port_is_list = True
            self.ports = set([int(port_number) for port_number in port.split(',') if int(port_number) > 0])

        elif len(port) == 1:
            self.from_port = self.to_port = int(port[0])
            self.ports = set(self.from_port)
            self.port_is_single = True

        else:
            raise TerraformComplianceInternalFailure('Unexpected situation. '
                                                     'Please report this port structure: {}'.format(port))


class SecurityGroup(object):
    def __init__(self, given_reqs, security_groups_in_plan):
        self.given = given_reqs
        self.sgs = security_groups_in_plan
        self.exact_match = False
        self.negative_match = True

        self.given_rule = SecurityGroupRule(**given_reqs)
        self.plan_rules = [SecurityGroupRule(**rule_data) for rule_data in security_groups_in_plan]

    def enable_exact_match(self):
        self.exact_match = True
        self.negative_match = False

    def enable_negative_match(self):
        self.exact_match = False
        self.negative_match = True

    def validate(self):

        for rule in self.plan_rules:
            # General Controls that is applicable for every scenario
            network_check = self._validate_network(rule.cidr_blocks)
            ports_check = self._validate_ports(rule)

    def _validate_network(self, cidr_in_plan):
        return is_ip_in_cidr(self.given_rule.cidr_blocks, cidr_in_plan)

    def _validate_ports(self, rule_data):
        if self.port_is_single:

