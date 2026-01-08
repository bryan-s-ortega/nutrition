terraform {
  backend "gcs" {
    bucket = "nutrition-app-tf-state" # UPDATE ME: User must create this bucket or change the name
    prefix = "terraform/state"
  }
}
