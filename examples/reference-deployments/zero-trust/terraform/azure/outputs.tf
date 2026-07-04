output "api_container_app_name" {
  value = azurerm_container_app.cavra_api.name
}

output "scanner_container_app_name" {
  value = azurerm_container_app.zero_trust_scanner.name
}

output "environment_id" {
  value = azurerm_container_app_environment.cavra.id
}
