terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Cloud SQL Instance
resource "google_sql_database_instance" "instance" {
  name             = "nutrition-db-instance"
  region           = var.region
  database_version = "POSTGRES_14"

  settings {
    tier = "db-f1-micro" # Smallest tier for development
  }

  deletion_protection = false # Set to true for production to prevent accidental deletion
}

# Database
resource "google_sql_database" "database" {
  name     = "nutrition_db"
  instance = google_sql_database_instance.instance.name
}

# User
resource "google_sql_user" "users" {
  name     = var.db_user
  instance = google_sql_database_instance.instance.name
  password = var.db_password
}

# Artifact Registry Repository
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "nutrition-backend"
  description   = "Docker repository for Nutrition App Backend"
  format        = "DOCKER"
}

# Cloud Run Service
resource "google_cloud_run_service" "backend" {
  name     = "nutrition-backend"
  location = var.region

  template {
    spec {
      containers {
        image = "us-docker.pkg.dev/cloudrun/container/hello" # Placeholder until we build our own

        env {
          name  = "DATABASE_URL"
          value = "postgresql://${var.db_user}:${var.db_password}@${google_sql_database_instance.instance.public_ip_address}:5432/nutrition_db"
          # Note: Public IP is easiest for now, but Cloud SQL Auth Proxy or VPC Connector is better for prod.
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Allow public access
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.backend.location
  project     = google_cloud_run_service.backend.project
  service     = google_cloud_run_service.backend.name
  policy_data = data.google_iam_policy.noauth.policy_data
}

