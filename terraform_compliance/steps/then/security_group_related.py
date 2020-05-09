# -*- coding: utf-8 -*-

from terraform_compliance.extensions.security_groups import SecurityGroup
from terraform_compliance.common.exceptions import TerraformComplianceInternalFailure
from terraform_compliance.common.error_handling import Error


def it_condition_have_proto_protocol_and_port_port_for_cidr(_step_obj, condition, proto, port, cidr):
    searching_for=dict(port=port, protocol=proto, cidr_blocks=cidr)

    for sg in _step_obj.context.stash:
        sg_obj = SecurityGroup(searching_for, sg['values'], address=sg['address'])
        if condition == 'must only':
            sg_obj.must_only_have()
        elif condition == 'must':
            sg_obj.must_have()
        elif condition == 'must not':
            sg_obj.must_not_have()
        else:
            raise TerraformComplianceInternalFailure('You can only use "must have", "must not have" and '
                                                     '"must only have" conditions on this step for now.'
                                                     'You tried to use "{}"'.format(condition))
        result, message = sg_obj.validate()

        if result is False:
            Error(_step_obj, message)

    return True