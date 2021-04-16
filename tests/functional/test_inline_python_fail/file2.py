# test functions go here
from terraform_compliance.common.error_handling import Error

def test_function(_step_obj):
	resources = _step_obj.context.stash
	for resource in resources:
		if resource['type'] == 'aws_vpc_peering_connection':
			if resource['values']['peer_vpc_id'] != resource['values']['vpc_id']:
				Error(_step_obj, "error message")
	return True


def dummy_function(_step_obj):
	return True