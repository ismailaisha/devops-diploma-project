output "app_server_ip" {
  description = "Публичный IP App Server"
  value       = aws_eip.app_server.public_ip
}

output "jenkins_ip" {
  description = "Публичный IP Jenkins Server"
  value       = aws_eip.jenkins.public_ip
}

output "app_server_id" {
  description = "ID App Server в AWS"
  value       = aws_instance.app_server.id
}

output "jenkins_id" {
  description = "ID Jenkins Server в AWS"
  value       = aws_instance.jenkins.id
}

output "s3_bucket_name" {
  description = "Имя S3 бакета для бэкапов"
  value       = aws_s3_bucket.backups.bucket
}

output "vpc_id" {
  description = "ID созданной VPC"
  value       = aws_vpc.main.id
}