output "network_self_link" {
  value       = google_compute_network.network.self_link
  description = "Self‑link of the created VPC"
}
