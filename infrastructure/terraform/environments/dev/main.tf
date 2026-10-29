# ============================================================
# CURRENT PUBLIC IP
# ============================================================

data "http" "my_ip" {
  url = "https://ipv4.icanhazip.com"
}

# ============================================================
# LOCAL SETTINGS
# ============================================================

locals {
  admin_ip = "${trimspace(data.http.my_ip.response_body)}/32"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }

  servers = {
    app = {
      name       = "${var.project_name}-app"
      size       = var.app_vm_size
      private_ip = cidrhost(var.subnet_address_prefixes[0], 10)
    }

    jenkins = {
      name       = "${var.project_name}-jenkins"
      size       = var.jenkins_vm_size
      private_ip = cidrhost(var.subnet_address_prefixes[0], 11)
    }
  }
}

# ============================================================
# RESOURCE GROUP
# ============================================================

resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-${var.environment}-rg"
  location = var.location
  tags     = local.tags
}

# ============================================================
# NETWORK
# ============================================================

resource "azurerm_virtual_network" "main" {
  name                = "${var.project_name}-vnet"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  address_space       = var.vnet_address_space
  tags                = local.tags
}

resource "azurerm_subnet" "servers" {
  name                 = "${var.project_name}-servers-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = var.subnet_address_prefixes
}

# ============================================================
# STATIC PUBLIC IP ADDRESSES
# ============================================================

resource "azurerm_public_ip" "servers" {
  for_each = local.servers

  name                = "${each.value.name}-pip"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  allocation_method = "Static"
  sku               = "Standard"

  tags = local.tags
}

# ============================================================
# NETWORK SECURITY GROUPS
# ============================================================

resource "azurerm_network_security_group" "servers" {
  for_each = local.servers

  name                = "${each.value.name}-nsg"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  tags = local.tags
}

# SSH from your current public IP to both servers
resource "azurerm_network_security_rule" "admin_ssh" {
  for_each = local.servers

  name                        = "Allow-Admin-SSH"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = local.admin_ip
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.servers[each.key].name
}

# WireGuard tunnel entry point on both servers
resource "azurerm_network_security_rule" "wireguard" {
  for_each = local.servers

  name                        = "Allow-WireGuard"
  priority                    = 110
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Udp"
  source_port_range           = "*"
  destination_port_range      = "51820"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.servers[each.key].name
}

# Public access to the application
resource "azurerm_network_security_rule" "app_web" {
  name                        = "Allow-HTTP-HTTPS"
  priority                    = 120
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_ranges     = ["80", "443"]
  source_address_prefix       = "Internet"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.servers["app"].name
}

# SSH deployment from Jenkins over the Azure private network
resource "azurerm_network_security_rule" "jenkins_to_app" {
  name                        = "Allow-Jenkins-SSH"
  priority                    = 130
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = "${local.servers.jenkins.private_ip}/32"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.servers["app"].name
}

# Jenkins UI accessible from your current public IP
resource "azurerm_network_security_rule" "jenkins_ui" {
  name                        = "Allow-Admin-Jenkins"
  priority                    = 120
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "8080"
  source_address_prefix       = local.admin_ip
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.servers["jenkins"].name
}

# Override the default broad inbound allowance within the VNet
resource "azurerm_network_security_rule" "deny_other_inbound" {
  for_each = local.servers

  name                        = "Deny-Other-Inbound"
  priority                    = 4096
  direction                   = "Inbound"
  access                      = "Deny"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.servers[each.key].name
}

# ============================================================
# NETWORK INTERFACES
# ============================================================

resource "azurerm_network_interface" "servers" {
  for_each = local.servers

  name                = "${each.value.name}-nic"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  ip_configuration {
    name                          = "primary"
    subnet_id                     = azurerm_subnet.servers.id
    private_ip_address_allocation = "Static"
    private_ip_address            = each.value.private_ip
    public_ip_address_id          = azurerm_public_ip.servers[each.key].id
  }

  tags = local.tags
}

resource "azurerm_network_interface_security_group_association" "servers" {
  for_each = local.servers

  network_interface_id      = azurerm_network_interface.servers[each.key].id
  network_security_group_id = azurerm_network_security_group.servers[each.key].id
}

# ============================================================
# UBUNTU VIRTUAL MACHINES
# ============================================================

resource "azurerm_linux_virtual_machine" "servers" {
  for_each = local.servers

  name                = each.value.name
  computer_name       = each.value.name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = each.value.size

  admin_username                  = var.admin_username
  disable_password_authentication = true

  network_interface_ids = [
    azurerm_network_interface.servers[each.key].id
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = file(pathexpand(var.ssh_public_key_path))
  }

  os_disk {
    name                 = "${each.value.name}-osdisk"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
    disk_size_gb         = 32
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "ubuntu-24_04-lts"
    sku       = "server"
    version   = "latest"
  }

  tags = merge(local.tags, {
    Role = each.key
  })

  depends_on = [
    azurerm_network_interface_security_group_association.servers,
    azurerm_network_security_rule.admin_ssh,
    azurerm_network_security_rule.wireguard,
    azurerm_network_security_rule.app_web,
    azurerm_network_security_rule.jenkins_to_app,
    azurerm_network_security_rule.jenkins_ui,
    azurerm_network_security_rule.deny_other_inbound
  ]
}