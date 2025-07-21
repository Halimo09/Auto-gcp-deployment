resource "google_container_cluster" "gke" {
  name               = var.cluster_name
  project            = var.project_id
  location           = var.location
  initial_node_count = var.initial_node_count

  # use the default node config
  node_config {
    machine_type = "e2-medium"
  }
}
