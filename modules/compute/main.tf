resource "google_compute_instance" "instances" {
  for_each     = toset(var.instance_names)
  name         = each.value
  project      = var.project_id
  zone         = var.zone
  machine_type = var.machine_type

  boot_disk {
    initialize_params { image = var.source_image }
  }
  network_interface {
    network = var.network
  }
  deletion_protection = false
}
