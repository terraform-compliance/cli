<img src='https://github.com/eerkunt/terraform-compliance/blob/master/logo.png' align=right height=100 valign=top><h1 align="center">terraform-compliance</h1>

<div align="center">
  <!-- Website -->
  <a href="https://terraform-compliance.com">
    <img src="https://img.shields.io/badge/website-https%3A%2F%2Fterraform--compliance.com-blue" alt="Website" />
  </a>
  
  <!-- Docker Ready -->
  <a href="https://hub.docker.com/r/eerkunt/terraform-compliance/">
    <img src="https://img.shields.io/badge/docker-ready-blue.svg?longCache=true&style=flat" alt="docker version is ready" />
  </a>

  <!-- License -->
  <a href="https://pypi.org/project/terraform-compliance/">
    <img src="https://img.shields.io/pypi/l/terraform-compliance.svg" alt="License" />
  </a>

  <!-- PyPI Version -->
  <a href="https://pypi.org/project/terraform-compliance/">
    <img src="https://img.shields.io/pypi/v/terraform-compliance.svg" alt="Package Version" />
  </a>
  
  <a href="https://pepy.tech/project/terraform-compliance">
    <img src="https://pepy.tech/badge/terraform-compliance" alt="Downloads" />
  </a>
</div>

<br />
<br />

`terraform-compliance` is a lightweight, security and compliance focused test framework against terraform to enable negative testing capability for your infrastructure-as-code.


- __compliance:__ Ensure the implemented code is following security standards, your own custom standards
- __behaviour driven development:__ We have BDD for nearly everything, why not for IaC ?
- __portable:__ just install it from `pip` or run it via `docker`. See [Installation](https://terraform-compliance.com/pages/installation/)
- __pre-deploy:__ it validates your code before it is deployed
- __easy to integrate:__ it can run in your pipeline (or in git hooks) to ensure all deployments are validated.
- __segregation of duty:__ you can keep your tests in a different repository where a separate team is responsible. 
- __why ?:__ why not ?

## Idea

`terraform-compliance` mainly focuses on [negative testing](https://en.wikipedia.org/wiki/Negative_testing) instead
of having fully-fledged [functional tests](https://en.wikipedia.org/wiki/Functional_testing) that are mostly used for
proving a component of code is performing properly. 

Fortunately, `terraform` is a marvellous abstraction layer for any API 
that __creates__/__updates__/__destroys__ entities. `terraform` also provides the 
[capability](https://www.terraform.io/docs/commands/plan.html#detailed-exitcode) 
to ensure everything is up-to-date between the local configuration and the remote API(s) responses. 

Given the fact, `terraform` is used mostly against Cloud APIs, what was missing is to ensure 
your code against your infrastructure must follow specific policies. Currently HashiCorp provides 
[Sentinel](https://www.hashicorp.com/sentinel/) for Enterprise Products. `terraform-compliance` is providing a 
similar functionality only for `terraform` while it is free-to-use and it is Open Source.

E.g. a sample policy could be, if you are working with `AWS`, you should not create an `S3 bucket`, 
without having any `encryption`. Of course, this is just an example which may or not be applicable 
for your case.

`terraform-compliance` provides a test framework to create these policies that will be executed against 
your [terraform plan](https://www.terraform.io/docs/commands/plan.html) in a context where both 
developers and security teams can understand easily while reading it, by applying [Behaviour Driven 
Development](https://en.wikipedia.org/wiki/Behavior-driven_development) Principles.

As returning back to the example, our example defined above will be translated into a BDD Feature 
and Scenario, as also seen in below ;

```
if you are working with AWS, you should not create an S3 bucket, without having any encryption
```

translates into ;

```gherkin
Given I have AWS S3 Bucket defined
Then it must contain server_side_encryption_configuration
```

`server_side_encryption_configuration` is coming from the terraform code, as shown below ;

```
resource "aws_s3_bucket" "b" {
  bucket = "my-bucket"
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = "${aws_kms_key.mykey.arn}"
        sse_algorithm     = "aws:kms"
      }
    }
  }
}
```

This policy ( Scenario ) will allow all S3 buckets newly created or updated must have encryption configuration set within the code. In an ideal way, this Scenario (among with all other Scenarios) will run on a CI/CD pipeline that will ensure that nothing is deployed by violating your policies.

See [Examples](https://terraform-compliance.com/pages/Examples/) for more sample use cases.

Regarding the feature file format - `radish` is used to parse files with extension `.feature` - https://radish.readthedocs.io/en/stable/tutorial.html

![Example Run](https://github.com/eerkunt/terraform-compliance/blob/master/terraform-compliance-demo.gif?raw=true)

## Supporting / Requirements

`terraform-compliance` only supports `terraform` 0.12.+. In order to use older versions of `terraform`,
you can use [0.6.4](https://github.com/eerkunt/terraform-compliance/releases/tag/0.6.4) of the tool, 
but many capabilities will not be supported and maintaining of `0.6.4` version is ended.

Some of the features that you will be missing can be listed as ;

- Complete `terraform` interpolations support
- `terraform` modules, variables and providers support.
- Any filtering function for advanced queries
- Many missing resources requires `tag`ging.
- .. and many more ..

You can have a look to the [CHANGELOG](https://github.com/eerkunt/terraform-compliance/blob/master/CHANGELOG.md)
for further information.

## License
[MIT](https://tldrlegal.com/license/mit-license)
