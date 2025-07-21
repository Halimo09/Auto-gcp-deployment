terraform {
  backend "gcs" {
    bucket = "mahmo-terraform-state-466619"
    prefix = "terraform-gcp-project"
  }
}
