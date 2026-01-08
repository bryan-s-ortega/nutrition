# Nutrition App

A full-stack mobile application for personalized meal planning, featuring **Dynamic Meal Generation** and automated **Cloud Infrastructure**.

## Tech Stack
-   **Backend**: Python (FastAPI, SQLModel)
-   **Frontend**: React Native (Expo)
-   **Cloud**: Google Cloud Run & SQL (Provisioned via **Terraform**)

## Quick Start
1.  **Start Backend** (Auto-connects to Cloud DB):
    ```bash
    just backend
    ```
2.  **Start Mobile App**:
    ```bash
    just mobile-web
    ```

## Development Commands
| Command | Description |
| :--- | :--- |
| `just backend` | Runs API + Cloud SQL Proxy |
| `just mobile-web` | Runs Frontend in Web Mode |
| `just test` | Runs Backend Unit Tests |
| `just lint` | Runs Linter & Formatter |
| `just destroy` | Destroys GCP Infrastructure |

## Documentation
-   [**Re-creation Guide**](./recreate_guide.md): How to rebuild infrastructure.