terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-2"
}

locals {
  name = "swns" # Service Name
  env  = "staging"
}

module "s3" {
  source = "../../modules/s3"

  name = local.name
  env  = local.env

}
