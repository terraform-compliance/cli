from radish import before, after, step
import terraform_validate
import os
import sys

@before.each_scenario
def init_terraform_files(step):
	if len(sys.argv) <= 2:
		raise Exception("Usage: radish <feature directory> <terraform files directory>")

	tf_dir = os.path.join(os.path.abspath(sys.argv[2]))
	step.context.validator = terraform_validate.Validator(tf_dir)