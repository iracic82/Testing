output "tenant_id" {
  description = "The Azure Tenant ID where the Infoblox Service Principal was created"
  value       = data.azurerm_client_config.current.tenant_id
}

output "service_principal_object_id" {
  description = "Object ID of the created Service Principal"
  value       = azuread_service_principal.infoblox_sp.id
}

output "subscription_id" {
  description = "The Azure Subscription ID where the role was assigned"
  value       = var.subscription_id
}
