# ============================================================
# GITHUB WEBHOOK IP RANGES
# ============================================================

data "http" "github_meta" {
  url = "https://api.github.com/meta"

  request_headers = {
    Accept = "application/vnd.github+json"
  }
}

locals {
  github_webhook_ipv4 = [
    for cidr in jsondecode(data.http.github_meta.response_body).hooks :
    cidr if !strcontains(cidr, ":")
  ]
}

# ============================================================
# GITHUB WEBHOOK ACCESS TO JENKINS
# ============================================================

resource "azurerm_network_security_rule" "github_webhook" {
  name                        = "Allow-GitHub-Webhooks"
  priority                    = 130
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "8080"
  source_address_prefixes     = local.github_webhook_ipv4
  destination_address_prefix  = "${local.servers.jenkins.private_ip}/32"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.servers["jenkins"].name

  lifecycle {
    precondition {
      condition     = length(local.github_webhook_ipv4) > 0
      error_message = "GitHub did not return any IPv4 webhook ranges."
    }
  }
}