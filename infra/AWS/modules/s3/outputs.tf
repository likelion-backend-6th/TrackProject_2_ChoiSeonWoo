output "bucket_regional_dns" {
  value = aws_s3_bucket.main.bucket_regional_domain_name
}
