from radish import before, world
from terraform_compliance import Validator
from terraform_compliance.extensions.terraform_validate import enable_resource_mounting


@before.each_feature
def load_terraform_data(feature):
    tf_conf = Validator(world.config.user_data['tf_dir'])
    tf_conf.enable_variable_expansion()

    # Custom extensions
    enable_resource_mounting(tf_conf.terraform_config)

    world.config.terraform = tf_conf
