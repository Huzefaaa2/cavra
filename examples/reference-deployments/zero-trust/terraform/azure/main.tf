terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.110"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "cavra" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_log_analytics_workspace" "cavra" {
  name                = "${var.name_prefix}-law"
  location            = azurerm_resource_group.cavra.location
  resource_group_name = azurerm_resource_group.cavra.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "cavra" {
  name                       = "${var.name_prefix}-env"
  location                   = azurerm_resource_group.cavra.location
  resource_group_name        = azurerm_resource_group.cavra.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.cavra.id
}

resource "azurerm_container_app" "cavra_api" {
  name                         = "${var.name_prefix}-api"
  container_app_environment_id = azurerm_container_app_environment.cavra.id
  resource_group_name          = azurerm_resource_group.cavra.name
  revision_mode                = "Single"

  ingress {
    external_enabled = var.external_ingress_enabled
    target_port      = 8000
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    container {
      name   = "cavra-api"
      image  = var.cavra_api_image
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "CAVRA_FAIL_CLOSED"
        value = "true"
      }
      env {
        name  = "CAVRA_TENANT_ID"
        value = var.tenant_id
      }
      env {
        name  = "CAVRA_WORKSPACE_ID"
        value = var.workspace_id
      }
    }
  }
}

resource "azurerm_container_app" "zero_trust_scanner" {
  name                         = "${var.name_prefix}-scanner"
  container_app_environment_id = azurerm_container_app_environment.cavra.id
  resource_group_name          = azurerm_resource_group.cavra.name
  revision_mode                = "Single"

  template {
    min_replicas = 0
    max_replicas = 1
    container {
      name   = "cavra-scanner"
      image  = var.scanner_image
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "CAVRA_SCANNER_MODE"
        value = "metadata_only"
      }
      env {
        name  = "CAVRA_FAIL_CLOSED"
        value = "true"
      }
      env {
        name  = "CAVRA_TENANT_ID"
        value = var.tenant_id
      }
      env {
        name  = "CAVRA_WORKSPACE_ID"
        value = var.workspace_id
      }
    }
  }
}
