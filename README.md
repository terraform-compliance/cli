# terraform-compliance
----------------------

A compliancy tool that runs against terraform files kept in local with BDD style configuration. 

This tool uses ;

* [radish-bdd](https://github.com/radish-bdd/radish)
* [terraform-validate](https://github.com/elmundio87/terraform_validate)

![Example Run](terraform-compliance-demo.gif)

### Installation
Clone this repository

	# git clone https://github.com/eeerkunt/terraform-compliance
	# cd terraform-compliance


(OPTIONAL) Create a virtualenv and activate it

	# virtualenv venv
	# source venv/bin/activate


Install requirements

	# pip install -r requirements.txt

and start playing

### Usage
Store your terraform files into any directory and pass that directory as an argument to radish.

For e.g. Assuming that your terraform files are stored in `/path/to/tf/files` and tests are stored in `./providers/aws`to run tests against it ;

	~# radish providers/aws /path/to/tf/files


All radish features are available

### Going further

The capabilities are stored in [radish](radish) directory where you can add any steps as a capability.

Tests, or _features/scenarios_ in radish-style, are stored in [providers](providers) directory.