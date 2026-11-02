# Kubernetes frontend: доступ с текущего публичного IP администратора.
resource "azurerm_network_security_rule" "admin_kubernetes_frontend" {
  name                        = "Allow-Admin-Kubernetes-Frontend"
  priority                    = 150
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "30080"
  source_address_prefix       = local.admin_ip
  destination_address_prefix  = local.servers.app.private_ip
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.servers["app"].name
}