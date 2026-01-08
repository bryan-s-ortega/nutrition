# Nutrition App

A comprehensive, full-stack mobile application for personalized meal planning, built with **FastAPI** and **React Native**. The project features automated infrastructure provisioning on **Google Cloud Platform** using **Terraform** and a robust CI/CD pipeline via **GitHub Actions**.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLModel.
- **Frontend**: React Native, Expo, Expo Router (Web + Mobile).
- **Database**: PostgreSQL (Production), SQLite (Development).
- **Infrastructure**: Terraform, Google Cloud Run, Cloud SQL, Artifact Registry.
- **CI/CD**: GitHub Actions (Linting, Testing, Terraform Plan/Apply).
- **Tooling**: `uv` (Python), `npm` (Node), `just` (Command Runner).

## Quick Start

We use `just` to automate common tasks.

1.  **Prerequisites**:
    - [uv](https://github.com/astral-sh/uv)
    - Node.js & npm
    - [Just](https://github.com/casey/just) (Optional, but recommended)

2.  **Start Backend**:
    Start the backend server to handle API requests.
    ```bash
    just backend
    ```

3.  **Run Application**:
    ```bash
    # Start Frontend (Web)
    just mobile-web
    ```
    Visit `http://localhost:8081` to use the app.

## Development

- **Linting & Formatting**:
    ```bash
    just lint
    ```
- **Tests**:
    ```bash
    just test
    ```
- **CI Check** (Simulate GitHub Actions):
    ```bash
    just ci
    ```

## Infrastructure & Deployment

The infrastructure is fully managed as code.

### Prerequisites
- Google Cloud Project.
- Service Account with `Owner` or specific permissions (`Cloud Run Admin`, `Cloud SQL Admin`, etc.).
- GCS Bucket for Terraform State (`nutrition-app-tf-state`).

### Deployment
Deployment is automated via GitHub Actions:
- **Pull Requests**: Runs `terraform plan` and backend tests.
- **Push to Main**: Runs `terraform apply` to deploy changes to Cloud Run.

### Manual Setup
See `deployment_guide.md` for details on setting up secrets (GCP_SA_KEY, etc.).