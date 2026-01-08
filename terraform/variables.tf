variable "project_id" {
  description = "The Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "The region to deploy resources in"
  type        = string
  default     = "us-central1"
}

variable "db_user" {
  description = "The database username"
  type        = string
  default     = "nutrition_user"
}

variable "db_password" {
  description = "The database password"
  type        = string
  sensitive   = true
}
