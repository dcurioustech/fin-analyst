# Terraform configuration for Financial Analysis Assistant GCP infrastructure

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

# Configure the Google Cloud Provider
provider "google" {
  project = var.project_id
  region  = var.region
}

# Variables
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# Enable required APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "firestore.googleapis.com",
    "redis.googleapis.com",
    "storage.googleapis.com",
    "monitoring.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudbuild.googleapis.com",
    "containerregistry.googleapis.com"
  ])
  
  service = each.value
  disable_on_destroy = false
}

# Firestore Database
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "financial-analyst-db"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
  
  depends_on = [google_project_service.apis]
}

# Redis instance for caching
resource "google_redis_instance" "cache" {
  name           = "financial-analysis-cache-${var.environment}"
  tier           = "BASIC"
  memory_size_gb = 1
  region         = var.region
  
  redis_version     = "REDIS_6_X"
  display_name      = "Financial Analysis Cache"
  
  depends_on = [google_project_service.apis]
}

# Cloud Storage bucket for file storage
resource "google_storage_bucket" "storage" {
  name     = "${var.project_id}-financial-analysis-${var.environment}"
  location = var.region
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
  
  depends_on = [google_project_service.apis]
}

# Service Account for Cloud Run
resource "google_service_account" "cloud_run_sa" {
  account_id   = "financial-analysis-${var.environment}"
  display_name = "Financial Analysis Service Account"
  description  = "Service account for Financial Analysis Assistant"
}

# IAM bindings for service account
resource "google_project_iam_member" "firestore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

resource "google_project_iam_member" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

resource "google_project_iam_member" "secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# Secrets for API keys
resource "google_secret_manager_secret" "google_api_key" {
  secret_id = "google-api-key-${var.environment}"
  
  replication {
    auto {}
  }
  
  depends_on = [google_project_service.apis]
}

resource "google_secret_manager_secret" "alpha_vantage_key" {
  secret_id = "alpha-vantage-key-${var.environment}"
  
  replication {
    auto {}
  }
  
  depends_on = [google_project_service.apis]
}

resource "google_secret_manager_secret" "polygon_key" {
  secret_id = "polygon-key-${var.environment}"
  
  replication {
    auto {}
  }
  
  depends_on = [google_project_service.apis]
}

# Note: Cloud Run service will be deployed via Cloud Build
# See cloudbuild.yaml for the actual deployment configuration

# Outputs
output "project_id" {
  description = "GCP Project ID"
  value       = var.project_id
}

output "redis_host" {
  description = "Redis instance host"
  value       = google_redis_instance.cache.host
}

output "storage_bucket" {
  description = "Storage bucket name"
  value       = google_storage_bucket.storage.name
}

output "service_account_email" {
  description = "Service account email"
  value       = google_service_account.cloud_run_sa.email
}