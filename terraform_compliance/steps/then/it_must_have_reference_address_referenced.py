# -*- coding: utf-8 -*-

from terraform_compliance.common.helper import (
    search_regex_in_list
)
from terraform_compliance.common.error_handling import Error
from terraform_compliance.common.exceptions import TerraformComplianceInternalFailure
from terraform_compliance.common.defaults import Defaults


def it_must_have_reference_address_referenced(_step_obj, reference_address):
    if _step_obj.context.stash:
        for resource in _step_obj.context.stash:
            if isinstance(resource, dict):
                if Defaults.r_mount_addr_ptr_list in resource and search_regex_in_list(reference_address,
                                                                                       resource[Defaults.r_mount_addr_ptr_list]):
                    return True
            else:
                raise TerraformComplianceInternalFailure('Unexpected resource structure: {}'.format(resource))

            Error(_step_obj, '{} is not referenced within {}.'.format(reference_address, resource.get('address')))
    else:
        Error(_step_obj, 'No entities found for this step to process. Check your filtering steps in this scenario.')
