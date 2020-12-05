resource "aws_kms_key" "mykey" {
  description             = "This key is used to encrypt bucket objects"
  deletion_window_in_days = 10
}

resource "aws_s3_bucket" "log_bucket" {
  bucket = "mybucket"
  acl    = "log-delivery-write"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = "$aws_kms_key.mykey.arn"
        sse_algorithm     = "aws:kms"
      }
    }
  }

  versioning {
    enabled = true
  }

}

resource "aws_s3_bucket" "mybucket" {
  bucket = "mybucket"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = "$aws_kms_key.mykey.arn"
        sse_algorithm     = "aws:kms"
      }
    }
  }

  logging {
    target_bucket = "$aws_s3_bucket.log_bucket.id"
    target_prefix = "log/"
  }

  versioning {
    enabled = true
  }

}


resource "aws_s3_bucket" "mybucket2" {
  bucket = "mybucket2"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = "$aws_kms_key.mykey.arn"
        sse_algorithm     = "aws:kms"
      }
    }
  }

  logging {
    target_bucket = "$aws_s3_bucket.log_bucket.id"
    target_prefix = "log/"
  }

}