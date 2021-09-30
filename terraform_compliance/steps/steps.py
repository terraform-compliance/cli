# -*- coding: utf-8 -*-

from radish import (
    world,
    given,
    when,
    then
)
from terraform_compliance.common.helper import (
    Null,
    EmptyStash
)
import re
from terraform_compliance.common.error_handling import Error

# GIVEN
from terraform_compliance.steps.given.i_have_name_section_configured import i_have_name_section_configured

# WHEN
from terraform_compliance.steps.when.its_key_metadata_has_something import its_key_metadata_has_something
from terraform_compliance.steps.when.its_key_is_value import (
    its_key_is_value,
    its_key_is_not_value
)
from terraform_compliance.steps.when.maths import (
    i_action_them,
    i_expect_the_result_is_operator_than_number
)
from terraform_compliance.steps.when.it_contains_something import (
    it_contains_something_old,
    it_has_something,
    it_does_not_have_something
)

# THEN
from terraform_compliance.steps.then.it_must_contain_something import (
    it_must_contain_something,
    it_must_not_contain_something,
)
from terraform_compliance.steps.then.property_is_enabled import property_is_enabled
from terraform_compliance.steps.then.security_group_related import it_condition_have_proto_protocol_and_port_port_for_cidr
from terraform_compliance.steps.then.its_value_condition_match_the_search_regex import its_value_condition_match_the_search_regex_regex
from terraform_compliance.steps.then.its_value_condition_match_the_search_regex import its_singular_value_condition_match_the_search_regex_regex
from terraform_compliance.steps.then.its_value_condition_match_the_search_regex import any_of_its_values_condition_match_the_search_regex_regex
from terraform_compliance.steps.then.its_value_condition_contain import its_value_condition_contain
from terraform_compliance.steps.then.it_must_have_reference_address_referenced import it_must_have_reference_address_referenced
from terraform_compliance.steps.then.its_key_condition_be_value import its_key_condition_be_value
from terraform_compliance.steps.then.interpolations import i_flatten_everything_found
from terraform_compliance.steps.then.it_must_be_in import it_must_be_in
from terraform_compliance.steps.then.it_must_not_be_in import it_must_not_be_in
from terraform_compliance.steps.then.its_value_condition_be_null import its_value_condition_be_null

# {name} is checked for startswith("resource that supports "). The @given decorator for that documented case is not needed
@given(u'I have {name:ANY} defined')
@given(u'I have {name:ANY} {type_name:SECTION} configured')
def wrapper(_step_obj, name, type_name='resource', _terraform_config=world):
    return i_have_name_section_configured(_step_obj, name, type_name, _terraform_config)


@when(u'its {key:PROPERTY} metadata has {value:PROPERTY}')
@when(u'its {key:PROPERTY} metadata is {value:PROPERTY}')
@when(u'its {key:PROPERTY} metadata contains {value:PROPERTY}')
@when(u'its {key:PROPERTY} metadata includes {value:PROPERTY}')
def wrapper(_step_obj, key, value):
    return its_key_metadata_has_something(_step_obj, key, value)


@when(u'its {key:PROPERTY} metadata has not {value:PROPERTY}')
@when(u'its {key:PROPERTY} metadata is not {value:PROPERTY}')
@when(u'its {key:PROPERTY} metadata does not have {value:PROPERTY}')
@when(u'its {key:PROPERTY} metadata does not contain {value:PROPERTY}')
@when(u'its {key:PROPERTY} metadata does not include {value:PROPERTY}')
def wrapper(_step_obj, key, value):
    return its_key_metadata_has_something(_step_obj, key, value, has_step=False)


@when(u'its {key:PROPERTY} is {value:PROPERTY}')
@when(u'its {key:PROPERTY} has {value:PROPERTY}')
@when(u'its {key:PROPERTY} includes {value:PROPERTY}')
@when(u'its {key:PROPERTY} contains {value:PROPERTY}')
@when(u'its {address:PROPERTY} {key:PROPERTY} is {value:PROPERTY}')
@when(u'its {address:PROPERTY} {key:PROPERTY} has {value:PROPERTY}')
@when(u'its {address:PROPERTY} {key:PROPERTY} includes {value:PROPERTY}')
@when(u'its {address:PROPERTY} {key:PROPERTY} contains {value:PROPERTY}')
@when(u'its {key:PROPERTY} includes an entry where {value:PROPERTY} is {dict_value:PROPERTY}')
def wrapper(_step_obj, key, value, dict_value=None, address=Null):
    return its_key_is_value(_step_obj, key, value, dict_value, address)


@when(u'its {key:PROPERTY} is not {value:PROPERTY}')
@when(u'its {key:PROPERTY} has not {value:PROPERTY}')
@when(u'its {key:PROPERTY} does not include {value:PROPERTY}')
@when(u'its {key:PROPERTY} does not contain {value:PROPERTY}')
@when(u'its {address:PROPERTY} {key:PROPERTY} is not {value:PROPERTY}')
@when(u'its {address:PROPERTY} {key:PROPERTY} has not {value:PROPERTY}')
@when(u'its {address:PROPERTY} {key:PROPERTY} does not include {value:PROPERTY}')
@when(u'its {address:PROPERTY} {key:PROPERTY} does not contain {value:PROPERTY}')
@when(u'its {key:PROPERTY} does not include an entry where {value:PROPERTY} is {dict_value:PROPERTY}')
def wrapper(_step_obj, key, value, dict_value=None, address=Null):
    return its_key_is_not_value(_step_obj, key, value, dict_value, address)


@when(u'it contain {something:PROPERTY}') # This is just here for not breaking backward compatibility. I know its wrong.
@when(u'it contains {something:PROPERTY}')
def wrapper(_step_obj, something, inherited_values=Null):
    return it_contains_something_old(_step_obj, something, inherited_values=Null)


@when(u'it has {something:PROPERTY}')
@when(u'they have {something:PROPERTY}')
def wrapper(_step_obj, something, inherited_values=Null):
    return it_has_something(_step_obj, something, inherited_values=Null)


@when(u'it does not contain {something:PROPERTY}')
@when(u'it doesnt contain {something:PROPERTY}')
@when(u'they do not have {something:PROPERTY}')
@when(u'they dont have {something:PROPERTY}')
@when(u'it does not have {something:PROPERTY}')
@when(u'it doesnt have {something:PROPERTY}')
def wrapper(_step_obj, something, inherited_values=Null):
    return it_does_not_have_something(_step_obj, something, inherited_values=Null)


@then(u'it must have "{reference_address}" referenced')
def wrapper(_step_obj, reference_address):
    return it_must_have_reference_address_referenced(_step_obj, reference_address)


@then(u'it {condition:ANY} have {proto} protocol and port {port} for {cidr:ANY}')
def wrapper(_step_obj, condition, proto, port, cidr):
    return it_condition_have_proto_protocol_and_port_port_for_cidr(_step_obj, condition, proto, port, cidr)


@then(u'it must contain {something:PROPERTY_COMPAT}')
@then(u'it must have {something:PROPERTY_COMPAT}')
@then(u'they must contain {something:PROPERTY_COMPAT}')
@then(u'they must have {something:PROPERTY_COMPAT}')
def wrapper(_step_obj, something, inherited_values=Null):
    return it_must_contain_something(_step_obj, something, inherited_values=Null)


@then(u'it must not contain {something:PROPERTY_COMPAT}')
@then(u'they must not contain {something:PROPERTY_COMPAT}')
@then(u'it must not have {something:PROPERTY_COMPAT}')
@then(u'they must not have {something:PROPERTY_COMPAT}')
def wrapper(_step_obj, something, inherited_values=Null):
    return it_must_not_contain_something(_step_obj, something, inherited_values=Null)


@then(u'{something:ANY} is enabled')
@then(u'{something:ANY} is be enabled')
@then(u'{something:ANY} must be enabled')
def wrapper(_step_obj, something):
    return property_is_enabled(_step_obj, something)


@when(u'I {action_type:PROPERTY} it')
@when(u'I {action_type:PROPERTY} them')
@when(u'I {action_type:PROPERTY} the value')
def wrapper(_step_obj, action_type):
    return i_action_them(_step_obj, action_type)


@then(u'its value must be {operator:ANY} than {number:d}')
@then(u'I expect the result is {operator:ANY} than {number:d}')
@then(u'its value must be {operator:ANY} to {number:d}')
@then(u'I expect the result is {operator:ANY} to {number:d}')
def wrapper(_step_obj, operator, number, _stash=EmptyStash):
    return i_expect_the_result_is_operator_than_number(_step_obj, operator, number, _stash=EmptyStash)


@then(u'its value {condition:ANY} match the "{search_regex}" regex')
@then(u'all of its values {condition:ANY} match the "{search_regex}" regex')
def wrapper(_step_obj, condition, search_regex, _stash=EmptyStash):
    return its_value_condition_match_the_search_regex_regex(_step_obj,
                                                                condition,
                                                                search_regex,
                                                                _stash=EmptyStash)


@then(u'its singular value {condition:ANY} match the "{search_regex}" regex')
def wrapper(_step_obj, condition, search_regex, _stash=EmptyStash):
    return its_singular_value_condition_match_the_search_regex_regex(_step_obj,
                                                                condition,
                                                                search_regex,
                                                                _stash=EmptyStash)


@then(u'any of its values {condition:ANY} match the "{search_regex}" regex')
def wrapper(_step_obj, condition, search_regex, _stash=EmptyStash):
    return any_of_its_values_condition_match_the_search_regex_regex(_step_obj,
                                                                condition,
                                                                search_regex,
                                                                _stash=EmptyStash)


@then(u'its value {condition:ANY} be null')
def wrapper(_step_obj, condition):
    return its_value_condition_be_null(_step_obj, condition)


@then(u'its value {condition:ANY} be {match:ANY}')
def its_value_condition_equal(_step_obj, condition, match, _stash=EmptyStash):
    if match not in ('null'):
        return its_value_condition_match_the_search_regex_regex(_step_obj,
                                                                condition,
                                                                "^" + re.escape(match) + "$",
                                                                _stash)


@then(u'its value {condition:ANY} contain {value:ANY}')
def wrapper(_step_obj, condition, value, _stash=EmptyStash):
    return its_value_condition_contain(_step_obj, condition, value, _stash=EmptyStash)


@then(u'the scenario fails')
@then(u'the scenario should fail')
@then(u'the scenario must fail')
@then(u'it fails')
@then(u'it should fail')
@then(u'it must fail')
def it_fails(_step_obj):
    Error(_step_obj, 'Forcefully failing the scenario on {} ({}) {}'.format(_step_obj.context.name,
                                                                            ', '.join(_step_obj.context.addresses),
                                                                            _step_obj.context.type))


@then('its {key:ANY} {condition:ANY} be {value:ANY}')
@then('its {key:ANY} property {condition:ANY} be {value:ANY}')
@then('its {key:ANY} key {condition:ANY} be {value:ANY}')
def wrapper(_step_obj, key, condition, value, stash=Null, depth=0):
    return its_key_condition_be_value(_step_obj, key, condition, value, stash=Null, depth=0)


@then('I flatten all values found')
def wrapper(_step_obj):
    return i_flatten_everything_found(_step_obj)

@then('it must be a subset of {haystack:ANY}')
@then('it must be in {haystack:ANY}')
def wrapper(_step_obj, haystack):
    return it_must_be_in(_step_obj, haystack)

@then('it must be a superset of {haystack:ANY}')
@then('it must cover {haystack:ANY}')
def wrapper(_step_obj, haystack):
    return it_must_be_in(_step_obj, haystack, cover=True)

@then('it must not be a subset of {haystack:ANY}')
@then('it must not be in {haystack:ANY}')
def wrapper(_step_obj, haystack):
    return it_must_not_be_in(_step_obj, haystack)

@then('it must not be a superset of {haystack:ANY}')
@then('it must not cover {haystack:ANY}')
def wrapper(_step_obj, haystack):
    return it_must_not_be_in(_step_obj, haystack, cover=True)