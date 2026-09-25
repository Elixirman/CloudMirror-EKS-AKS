resource "random_password" "azure_db" {
  length  = 20
  special = false
}

resource "azurerm_postgresql_flexible_server" "this" {
  name                   = "${var.project_name}-pg"
  resource_group_name    = azurerm_resource_group.this.name
  location               = "westus2"
  version                = "16"
  administrator_login    = "appuser"
  administrator_password = random_password.azure_db.result

  storage_mb = 32768
  sku_name   = "B_Standard_B1ms"

  public_network_access_enabled = true
}

resource "azurerm_postgresql_flexible_server_database" "this" {
  name      = "appdb"
  server_id = azurerm_postgresql_flexible_server.this.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure" {
  name             = "AllowAzureServices"
  server_id        = azurerm_postgresql_flexible_server.this.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

output "azure_db_host" {
  value = azurerm_postgresql_flexible_server.this.fqdn
}

output "azure_db_password" {
  value     = random_password.azure_db.result
  sensitive = true
}
