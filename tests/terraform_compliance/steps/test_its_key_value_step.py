import json
import pytest
from pathlib import Path
from terraform_compliance.steps.steps import (
    its_key_is_value, 
    its_key_is_not_value,
)
from tests.mocks import MockedStep, MockedWorld
from mock import patch

class ItsKeyValueTestCase:
    pass

def _get_test_cases():
    def build_test_case(p):
        with p.open() as f:
            j = json.load(f)
            test_case = ItsKeyValueTestCase()
            test_case.name = p.stem
            test_case.stash = j['stash']
            test_case.args = j['args']
            test_case.expected_ids = set(j['expected_ids'])
            return test_case

    path = Path(__file__).parent / 'its_key_value_test_cases'
    for p in path.rglob('*.json'):
        yield build_test_case(p)

class TestItsKeyValueStepCases():
    @pytest.mark.parametrize("test_case", list(_get_test_cases()), ids=lambda x: x.name)
    def test_its_key_is_value(self, test_case):
        step = MockedStep()
        step.context.stash = test_case.stash

        with patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld()):
            its_key_is_value(step, *test_case.args)

        assert step.state == ('passed' if test_case.expected_ids else 'skipped')

        if test_case.expected_ids:
            actual_ids = set(o['id'] for o in step.context.stash)
            assert actual_ids == test_case.expected_ids

    @pytest.mark.skip()
    @pytest.mark.parametrize("test_case", list(_get_test_cases()), ids=lambda x: x.name)
    def test_its_key_is_not_value(self, test_case):
        step = MockedStep()
        step.context.stash = test_case.stash

        with patch('terraform_compliance.extensions.ext_radish_bdd.world', return_value=MockedWorld()):
            its_key_is_not_value(step, *test_case.args)

        def collect_ids(val):
            if isinstance(val, dict):
                for k, v in val.items():
                    if k == 'id':
                        yield v
                    else: 
                        yield from collect_ids(v)
            elif isinstance(val, list):
                for child in val:
                    yield from collect_ids(child)

        all_ids = set(collect_ids(test_case.stash))
        expected_ids = all_ids - test_case.expected_ids

        assert step.state == ('passed' if expected_ids else 'skipped')
        
        if expected_ids:
            actual_ids = set(o['id'] for o in step.context.stash)
            assert actual_ids == expected_ids
