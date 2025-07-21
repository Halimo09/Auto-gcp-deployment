variable "project_id" {
  type        = string
  description = "GCP project ID to manage"
}

variable "organization_id" {
  type        = string
  description = "GCP organization ID"
}

variable "billing_account" {
  type        = string
  description = "GCP billing account to attach"
}

variable "google_credentials_path" {
  type        = string
  description = "Path to GCP service‑account JSON key"
}

variable "region" {
  type        = string
  description = "GCP region for resources"
  default     = "us-central1"
}

variable "zone" {
  type        = string
  description = "GCP zone for zonal resources"
  default     = "us-central1-a"
}

# Networking
variable "network_name" {
  type        = string
  description = "Name of the VPC network"
  default     = "default-network"
}
variable "auto_create_subnetworks" {
  type        = bool
  description = "Whether to auto-create subnetworks"
  default     = true
}

# Compute
variable "instance_names" {
  type        = list(string)
  description = "List of Compute Instance names"
  default     = []
}
variable "machine_type" {
  type        = string
  description = "Compute instance machine type"
  default     = "e2-medium"
}
variable "source_image" {
  type        = string
  description = "Boot disk image"
  default     = "debian-cloud/debian-11"
}

# Storage
variable "bucket_names" {
  type        = list(string)
  description = "List of Cloud Storage bucket names"
  default     = []
}

# Database
variable "database_instance_name" {
  type        = string
  description = "Cloud SQL instance name"
  default     = ""
}
variable "database_version" {
  type        = string
  description = "SQL engine version"
  default     = "POSTGRES_14"
}
variable "tier" {
  type        = string
  description = "SQL instance tier"
  default     = "db-f1-micro"
}

# Kubernetes
variable "cluster_name" {
  type        = string
  description = "GKE cluster name"
  default     = ""
}
variable "initial_node_count" {
  type        = number
  description = "Number of GKE nodes"
  default     = 1
}
