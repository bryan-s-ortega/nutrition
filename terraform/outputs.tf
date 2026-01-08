output "database_connection_name" {
  value = google_sql_database_instance.instance.connection_name
}

output "database_public_ip" {
  value = google_sql_database_instance.instance.public_ip_address
}

output "cloud_run_url" {
  value = google_cloud_run_service.backend.status[0].url
}
