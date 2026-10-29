variable "subscription_id" {
  description = "ID подписки Azure"
  type        = string
}

variable "project_name" {
  description = "Название проекта"
  type        = string
  default     = "fitflow"
}

variable "environment" {
  description = "Окружение проекта"
  type        = string
  default     = "dev"
}

variable "location" {
  description = "Регион Azure"
  type        = string
  default     = "southcentralus"
}

variable "app_vm_size" {
  description = "Размер виртуальной машины приложения"
  type        = string
  default     = "Standard_D2als_v6"
}

variable "jenkins_vm_size" {
  description = "Размер виртуальной машины Jenkins"
  type        = string
  default     = "Standard_F1as_v7"
}

variable "admin_username" {
  description = "Пользователь для подключения к серверам по SSH"
  type        = string
  default     = "devops"
}

variable "ssh_public_key_path" {
  description = "Путь к публичному SSH-ключу на локальном компьютере"
  type        = string
}

variable "vnet_address_space" {
  description = "Адресное пространство виртуальной сети Azure"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "subnet_address_prefixes" {
  description = "Диапазон адресов подсети серверов"
  type        = list(string)
  default     = ["10.0.1.0/24"]
}