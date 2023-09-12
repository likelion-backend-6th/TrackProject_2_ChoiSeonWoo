variable "ncp_access_key" {
  type = string
}

variable "ncp_secret_key" {
  type = string
}

variable "username" {
  type      = string
  sensitive = true
}


variable "password" {
  type      = string
  sensitive = true
}


variable "postgres_db" {
  type = string
}


variable "postgres_user" {
  type      = string
  sensitive = true
}


variable "postgres_password" {
  type      = string
  sensitive = true
}


variable "postgres_volume" {
  type = string
}


variable "db_container_name" {
  type = string
}

variable "django_settings_module" {
  type = string
}

variable "django_secret_key" {
  type = string
}

variable "django_container_name" {
  type = string
}

variable "ncr_host" {
  type = string
}

variable "ncr_image" {
  type = string
}

variable "ncp_lb_domain" {
  type = string
}

variable "ncp_s3_bucket_name" {
  type = string
}

variable "aws_access_key_id" {
  type = string
}

variable "aws_secret_access_key" {
  type = string
}

variable "aws_storage_bucket_name" {
  type = string
}

