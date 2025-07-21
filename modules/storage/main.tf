resource "google_storage_bucket" "buckets" {
  for_each = toset(var.bucket_names)
  name     = each.value
  project  = var.project_id
  location = var.location
}
