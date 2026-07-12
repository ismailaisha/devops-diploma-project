variable "aws_region" {
  type = string
  default = "us-east-2"
}

variable "project_name" {
    type = string
    default = "fitflow"
  
}

variable "environment" {
    type = string
    default = "dev"
  
}

variable "ssh_key_name" {
    type = string
    default = "fitflow-key"
  
}

variable "my_ip" {
    type = string
  
}

variable "s3_bucket_name" {
    type = string
    default = "fitflow-backups-080403789929"
}