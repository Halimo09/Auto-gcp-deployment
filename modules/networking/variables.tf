variable "project_id" {
  type        = string
  description = "GCP project ID"
}
variable "network_name" {
  type        = string
  description = "VPC network name"
}
variable "auto_create_subnetworks" {
  type        = bool
  description = "Auto‑create subnets"
}
