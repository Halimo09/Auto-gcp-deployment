output "instance_self_links" {
  value       = [for inst in google_compute_instance.instances : inst.self_link]
  description = "Self‑links of all instances"
}
