from radish import before, world
from terraform_compliance import Validator


@before.each_feature
def load_terraform_data(feature):
    v = Validator(world.config.user_data['tf_dir'])
    v.enable_variable_expansion()
    world.config.terraform = v
