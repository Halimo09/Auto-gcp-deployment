resource "google_sql_database_instance" "db" {
  name             = var.instance_name
  project          = var.project_id
  region           = var.region
  database_version = var.database_version

  settings {
    tier = var.tier
  }
  deletion_protection = false
}
