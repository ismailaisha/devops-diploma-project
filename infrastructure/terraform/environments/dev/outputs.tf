output "app_server_ip" {
  description = "Публичный IP App Server"
  value       = azurerm_public_ip.servers["app"].ip_address
}

output "jenkins_ip" {
  description = "Публичный IP Jenkins Server"
  value       = azurerm_public_ip.servers["jenkins"].ip_address
}

output "app_private_ip" {
  description = "Внутренний IP App Server"
  value       = azurerm_network_interface.servers["app"].private_ip_address
}

output "jenkins_private_ip" {
  description = "Внутренний IP Jenkins Server"
  value       = azurerm_network_interface.servers["jenkins"].private_ip_address
}

output "app_server_id" {
  description = "ID App Server в Azure"
  value       = azurerm_linux_virtual_machine.servers["app"].id
}

output "jenkins_id" {
  description = "ID Jenkins Server в Azure"
  value       = azurerm_linux_virtual_machine.servers["jenkins"].id
}

output "resource_group_name" {
  description = "Имя группы ресурсов Azure"
  value       = azurerm_resource_group.main.name
}

output "vnet_id" {
  description = "ID виртуальной сети Azure"
  value       = azurerm_virtual_network.main.id
}