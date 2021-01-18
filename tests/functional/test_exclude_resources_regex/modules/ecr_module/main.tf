variable "name" {
  type = string
}

variable "scan_on_push" {
  type    = string
  default = true
}

resource "aws_ecr_repository" "ecr_repository" {
  name                 = var.name
  image_tag_mutability =  "IMMUTABLE" 

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }

}

output "ecr_name" {
  value = aws_ecr_repository.ecr_repository.id
}
