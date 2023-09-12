terraform {
  required_providers {
    ncloud = {
      source = "NaverCloudPlatform/ncloud"
    }
    ssh = {
      source  = "loafoe/ssh"
      version = "2.6.0"
    }
  }
  required_version = ">= 0.13"
}

provider "ncloud" {
  access_key  = var.ncp_access_key
  secret_key  = var.ncp_secret_key
  region      = "KR"
  site        = "public"
  support_vpc = true
}

locals {
  env                       = "staging"
  subnet_netnum             = 1
  subnet_type               = "PUBLIC"
  db_name                   = "db"
  db_port_range             = "5432"
  db_init_script_path       = "db_init_script.tftpl"
  be_name                   = "be"
  be_port_range             = "8000"
  be_init_script_path       = "be_init_script.tftpl"
  server_image_product_code = "SW.VSVR.OS.LNX64.UBNTU.SVR2004.B050"
  ncp_s3_endpoint_url       = "https://kr.object.ncloudstorage.com"
  ncp_s3_region_name        = "kr-standard"
  aws_region                = "ap-northeast-2"
}

data "ncloud_server_product" "product" {
  server_image_product_code = local.server_image_product_code

  filter {
    name   = "product_code"
    values = ["SSD"]
    regex  = true
  }

  filter {
    name   = "cpu_count"
    values = ["2"]
  }

  filter {
    name   = "memory_size"
    values = ["4GB"]
  }

  filter {
    name   = "base_block_storage_size"
    values = ["50GB"]
  }

  filter {
    name   = "product_type"
    values = ["HICPU"]
  }
}


module "network" {
  source = "../../modules/network"

  ncp_access_key = var.ncp_access_key
  ncp_secret_key = var.ncp_secret_key
  env            = local.env
  subnet_netnum  = local.subnet_netnum
  subnet_type    = local.subnet_type
}

module "db" {
  source           = "../../modules/server"
  ncp_access_key   = var.ncp_access_key
  ncp_secret_key   = var.ncp_secret_key
  name             = local.db_name
  env              = local.env
  vpc_id           = module.network.vpc_id
  subnet_id        = module.network.subnet_id
  port_range       = local.db_port_range
  init_script_path = local.db_init_script_path
  init_script_envs = {
    username          = var.username
    password          = var.password
    postgres_db       = var.postgres_db
    postgres_user     = var.postgres_user
    postgres_password = var.postgres_password
    postgres_port     = local.db_port_range
    postgres_volume   = var.postgres_volume
    db_container_name = var.db_container_name
  }
  server_image_product_code = local.server_image_product_code
  server_product_code       = data.ncloud_server_product.product.product_code
}

module "be" {
  source           = "../../modules/server"
  ncp_access_key   = var.ncp_access_key
  ncp_secret_key   = var.ncp_secret_key
  name             = local.be_name
  env              = local.env
  vpc_id           = module.network.vpc_id
  subnet_id        = module.network.subnet_id
  port_range       = local.be_port_range
  init_script_path = local.be_init_script_path
  init_script_envs = {
    username                = var.username
    password                = var.password
    django_settings_module  = var.django_settings_module
    django_secret_key       = var.django_secret_key
    django_container_name   = var.django_container_name
    ncr_host                = var.ncr_host
    ncr_image               = var.ncr_image
    ncp_access_key          = var.ncp_access_key
    ncp_secret_key          = var.ncp_secret_key
    ncp_lb_domain           = var.ncp_lb_domain
    postgres_db             = var.postgres_db
    postgres_user           = var.postgres_user
    postgres_password       = var.postgres_password
    postgres_port           = local.db_port_range
    db_host                 = ncloud_public_ip.db_public_ip.public_ip
    ncp_s3_endpoint_url     = local.ncp_s3_endpoint_url
    ncp_s3_region_name      = local.ncp_s3_region_name
    ncp_s3_bucket_name      = var.ncp_s3_bucket_name
    aws_access_key_id       = var.aws_access_key_id
    aws_secret_access_key   = var.aws_secret_access_key
    aws_region              = local.aws_region
    aws_storage_bucket_name = var.aws_storage_bucket_name
  }
  server_image_product_code = local.server_image_product_code
  server_product_code       = data.ncloud_server_product.product.product_code
}

module "loadBalancer" {
  source             = "../../modules/loadBalancer"
  ncp_access_key     = var.ncp_access_key
  ncp_secret_key     = var.ncp_secret_key
  vpc_id             = module.network.vpc_id
  subnet_id          = module.network.subnet_id
  name               = local.be_name
  env                = local.env
  server_instance_no = module.be.server_instance_no
}

resource "ncloud_public_ip" "db_public_ip" {
  server_instance_no = module.db.server_instance_no
}

resource "ncloud_public_ip" "be_public_ip" {
  server_instance_no = module.be.server_instance_no
}


resource "ssh_resource" "init_db" {
  depends_on = [module.db]
  when       = "create"

  host     = ncloud_public_ip.db_public_ip.public_ip
  user     = var.username
  password = var.password

  timeout     = "1m"
  retry_delay = "5s"

  file {
    source      = "${path.module}/../../script/set_db_server.sh"
    destination = "/home/${var.username}/init.sh"
    permissions = "0700"
  }

  commands = [
    "/home/${var.username}/init.sh"
  ]
}

resource "ssh_resource" "init_be" {
  depends_on = [module.be]
  when       = "create"

  host     = ncloud_public_ip.be_public_ip.public_ip
  user     = var.username
  password = var.password

  timeout     = "1m"
  retry_delay = "5s"

  file {
    source      = "${path.module}/../../script/set_be_server.sh"
    destination = "/home/${var.username}/init.sh"
    permissions = "0700"
  }

  commands = [
    "/home/${var.username}/init.sh"
  ]
}
