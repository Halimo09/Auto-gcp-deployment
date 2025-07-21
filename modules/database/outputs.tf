output "connection_name" {
  value       = google_sql_database_instance.db.connection_name
  description = "Cloud SQL connection name"
}
