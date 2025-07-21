output "bucket_urls" {
  value       = [for b in google_storage_bucket.buckets : b.url]
  description = "URLs for all buckets"
}
