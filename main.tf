# 1. Create a VPC network
module "networking" {
  source                  = "./modules/networking"
  project_id              = var.project_id
  network_name            = var.network_name
  auto_create_subnetworks = var.auto_create_subnetworks
}

# 2. Provision Compute Instances
module "compute" {
  source         = "./modules/compute"
  project_id     = var.project_id
  zone           = var.zone
  network        = module.networking.network_self_link
  instance_names = var.instance_names
  machine_type   = var.machine_type
  source_image   = var.source_image
}

# 3. Create Storage Buckets
module "storage" {
  source       = "./modules/storage"
  project_id   = var.project_id
  bucket_names = var.bucket_names
  location     = var.region
}

# 4. Cloud SQL Database
module "database" {
  source             = "./modules/database"
  project_id         = var.project_id
  region             = var.region
  instance_name      = var.database_instance_name
  database_version   = var.database_version
  tier               = var.tier
}

# 5. GKE Cluster
module "kubernetes" {
  source             = "./modules/kubernetes"
  project_id         = var.project_id
  location           = var.zone
  cluster_name       = var.cluster_name
  initial_node_count = var.initial_node_count
}
