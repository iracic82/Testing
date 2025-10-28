######################################
# main.tf
######################################
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

provider "azuread" {}

variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}

variable "infoblox_app_id" {
  description = "Infoblox Application (Client) ID from Infoblox Portal"
  type        = string
}

# Create the Service Principal in your tenant for Infoblox App
resource "azuread_service_principal" "infoblox_sp" {
  client_id = var.infoblox_app_id
}

# Required for tenant_id output
data "azurerm_client_config" "current" {}

resource "azurerm_role_definition" "infoblox_dns_role" {
  name  = "Infoblox Full DNS Management"
  scope = "/subscriptions/${var.subscription_id}"

  permissions {
    actions = [
      "*/read",
      "Microsoft.Network/dnsZones/*",
      "Microsoft.Network/dnsResolvers/*",
      "Microsoft.Network/dnsForwardingRulesets/*",
      "Microsoft.Network/virtualNetworks/read",
      "Microsoft.Network/virtualNetworks/listDnsResolvers/action",
      "Microsoft.Network/virtualNetworks/subnets/read",
      "Microsoft.Network/virtualNetworks/subnets/join/action"
    ]
    not_actions = []
  }

  assignable_scopes = [
    "/subscriptions/${var.subscription_id}"
  ]
}

resource "azurerm_role_assignment" "assign_dns_role_to_infoblox" {
  scope              = azurerm_role_definition.infoblox_dns_role.scope
  role_definition_id = azurerm_role_definition.infoblox_dns_role.role_definition_resource_id
  principal_id       = azuread_service_principal.infoblox_sp.id
}
