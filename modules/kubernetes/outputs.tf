output "endpoint" {
  value       = google_container_cluster.gke.endpoint
  description = "GKE cluster endpoint"
}
