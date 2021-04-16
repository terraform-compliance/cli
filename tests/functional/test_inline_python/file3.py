# test functions go here
from terraform_compliance.common.error_handling import Error

def test_function(_step_obj):
	resources = _step_obj.context.stash
	_step_obj.context.stash = [{
	'mode': 'custom',
	'address': 'none',
	'name': 'my_object',
	'values': {
		'description': 'I have complete control over my tests'
	}

	}]
	return True