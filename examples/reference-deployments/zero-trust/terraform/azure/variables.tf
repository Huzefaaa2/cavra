variable "resource_group_name" {
  type        = string
  description = "Resource group for the CAVRA zero-trust reference deployment."
}

variable "location" {
  type        = string
  description = "Azure region."
  default     = "eastus"
}

variable "name_prefix" {
  type        = string
  description = "Name prefix for Azure resources."
  default     = "cavra-zt"
}

variable "tenant_id" {
  type        = string
  description = "CAVRA tenant scope."
}

variable "workspace_id" {
  type        = string
  description = "CAVRA workspace scope."
}

variable "cavra_api_image" {
  type        = string
  description = "CAVRA API container image."
}

variable "scanner_image" {
  type        = string
  description = "Customer-side scanner container image."
  default     = "python:3.12-slim"
}

variable "external_ingress_enabled" {
  type        = bool
  description = "Set false for private network mode."
  default     = false
}
