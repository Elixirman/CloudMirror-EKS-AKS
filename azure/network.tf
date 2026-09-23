resource "azurerm_resource_group" "this" {
  name     = "${var.project_name}-rg"
  location = var.location
}

resource "azurerm_virtual_network" "this" {
  name                = "${var.project_name}-vnet"
  address_space       = ["10.1.0.0/16"]
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
}

resource "azurerm_subnet" "aks" {
  name                 = "aks-subnet"
  resource_group_name  = azurerm_resource_group.this.name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = ["10.1.1.0/24"]
}
