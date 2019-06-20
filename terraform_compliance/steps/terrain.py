from radish import before, world
from terraform_compliance.extensions.terraform import TerraformParser


@before.each_feature
def load_terraform_data(feature):
    world.config.terraform = TerraformParser(world.config.user_data['plan_file'])
