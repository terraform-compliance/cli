import re
import sys
from terraform_compliance.common.helper import generate_target_resource
from terraform_compliance.common.helper import change_value_in_dict

if sys.version_info[0] > 2:
    unicode = str


def enable_resource_mounting(tf_conf, processing_resource=None, resource=None):
    if not resource:
        resource = 'resource'
    else:
        resource = resource.strip()

    if not processing_resource:
        if resource not in tf_conf:
            return

        processing_resource = tf_conf[resource]


    source = resource.strip()
    source = (source[:-3] if source.endswith('.id') else source)

    for sub_resource, sub_value in list(processing_resource.items()):

        if type(sub_value) is dict:
            enable_resource_mounting(tf_conf, sub_value, sub_resource)
        else:
            regex = r'\${(.*)\}'
            if type(sub_value) is str or type(sub_value) is unicode:
                matches = re.match(regex, sub_value)

                if matches is not None and not matches.group(1).startswith(('var', 'data', 'module')) and '(' not in matches.group(1):
                    target = generate_target_resource(matches.group(1))
                    change_value_in_dict(tf_conf, target, {source: processing_resource})

            elif type(sub_value) is list:
                for value in sub_value:
                    if type(value) is str or type(value) is unicode:
                        matches = re.match(regex, value)
                        if matches is not None and not matches.group(1).startswith(('var', 'data', 'module')) and '(' not in matches.group(1):
                                target = generate_target_resource(matches.group(1))
                                change_value_in_dict(tf_conf, target, {source: processing_resource})


def normalise_tag_values(property_list):
    for property_object in property_list.properties:
        if type(property_object.property_value) is not dict():
            property_object.property_value = dict(normalised=property_object.property_value)