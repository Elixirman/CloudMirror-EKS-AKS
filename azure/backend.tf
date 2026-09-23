terraform {
  required_version = ">= 1.5"

  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "ogplatformtfstate21244"
    container_name        = "tfstate"
    key                    = "azure/terraform.tfstate"
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}
