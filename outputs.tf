output "network_self_link" {
  value       = module.networking.network_self_link
  description = "Self‑link of the VPC network"
}

output "instance_self_links" {
  value       = module.compute.instance_self_links
  description = "Self‑links of the compute instances"
}

output "bucket_urls" {
  value       = module.storage.bucket_urls
  description = "URLs of the created buckets"
}

output "sql_connection_name" {
  value       = module.database.connection_name
  description = "Connection name for Cloud SQL instance"
}

output "gke_endpoint" {
  value       = module.kubernetes.endpoint
  description = "GKE cluster endpoint"
}
