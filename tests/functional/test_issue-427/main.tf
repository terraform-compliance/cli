# Courtesy of @luis-calvo-mackenna at https://github.com/terraform-compliance/cli/issues/427#issuecomment-754226668

# Configure the AWS Provider
provider "aws" {
  region = "us-west-1"
  version = "~> 3.4.0"
}

terraform {
  required_version = "~> 0.13.3"
}


# DNS
resource "aws_route53_zone" "public" {
  name = "misayu.cl"

  tags = {
    Name = "app-name-aws-route53-zone-public-${terraform.workspace}"
    Environment = terraform.workspace
  }
}

locals {
  domains = ["www.misayu.cl", "misayu.cl"]
}

resource "aws_route53_record" "domains_alias" {
  count = length(local.domains)
  zone_id = aws_route53_zone.public.zone_id
  name    = local.domains[count.index]
  type    = "A"

  alias {
    name                   = "aws_alb_dns_name"
    zone_id                = "aws_alb_zone_id"
    evaluate_target_health = true
  }
}


resource "aws_route53_record" "sayu_cert_validation_record" {
  count = 1
  allow_overwrite = true
  name            =  tolist(aws_acm_certificate.sayu_cert.domain_validation_options)[0].resource_record_name
  records         = [ tolist(aws_acm_certificate.sayu_cert.domain_validation_options)[0].resource_record_value ]
  ttl             = 60
  type            = tolist(aws_acm_certificate.sayu_cert.domain_validation_options)[0].resource_record_type
  zone_id         = aws_route53_zone.public.zone_id
}

resource "aws_acm_certificate_validation" "sayu_cert_validation" {
  depends_on = [aws_acm_certificate.sayu_cert, aws_route53_record.sayu_cert_validation_record]

  certificate_arn         = aws_acm_certificate.sayu_cert.arn
  validation_record_fqdns = [ for record in aws_route53_record.sayu_cert_validation_record : record.fqdn ]
}


# Certificate configuration
resource "aws_acm_certificate" "sayu_cert" {
  domain_name       = "*.misayu.cl"
  validation_method = "DNS"
  subject_alternative_names = ["misayu.cl"]

  tags = {
     Name = "app_name-aws-acm-certificate-sayu-cert-${terraform.workspace}"
    Environment = terraform.workspace
  }

  lifecycle {
    create_before_destroy = true
  }
}