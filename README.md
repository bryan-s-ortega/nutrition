# Nutrition App

A comprehensive mobile application for personalized meal planning and nutritional tracking, compatible with Android, iOS, and Web. The app uses nutritional theory to generate caloric and macro targets based on user objectives (Weight Loss, Muscle Gain, Maintenance).

## Tech Stack

- **Backend**: Python (FastAPI), SQLModel, SQLite (Dev)
- **Frontend**: React Native, Expo, Expo Router (Web + Mobile support)
- **Tooling**: `uv` (Python package management), `npm`

## Features

- **Onboarding**: Collects user biometrics (Age, Weight, Height, Gender) and objectives.
- **Nutritional Engine**: Calculates BMR (Mifflin-St Jeor) and TDEE to generate precise Macro targets.
- **Premium UI**: Modern, clean interface with visual data representation.
- **Cross-Platform**: Runs seamlessly on Web, Android, and iOS.

## Getting Started

### Prerequisites

- Python 3.10+ and [uv](https://github.com/astral-sh/uv)
- Node.js & npm

### Backend Setup

The backend handles the nutritional logic and user data persistence.

1.  **Navigate to Project Root**:
    ```bash
    cd nutrition
    ```

2.  **Install Dependencies & Run**:
    This project is configured to run with `uv`.
    ```bash
    # Run the server (auto-installs dependencies in a virtual environment)
    uv run uvicorn backend.main:app --reload
    ```

    *Alternatively, using standard pip:*
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    uvicorn backend.main:app --reload
    ```

3.  **Run Tests**:
    Verify the nutritional logic.
    ```bash
    uv run pytest backend/tests
    ```

### Frontend Setup (Mobile/Web)

The frontend is built with Expo and can run in a browser or on a device.

1.  **Navigate to Mobile Directory**:
    ```bash
    cd mobile
    ```

2.  **Install Dependencies**:
    ```bash
    npm install
    ```

3.  **Run the App**:
    
    *   **Web Browser** (Recommended for quick testing):
        ```bash
        npm run web
        ```
    
    *   **Android/iOS**:
        Requires Android Studio or Xcode to be configured.
        ```bash
        npm run android
        # OR
        npm run ios
        ```

## Project Structure

- `backend/`: FastAPI service.
    - `main.py`: Entry point.
    - `models.py`: Database models (User, MealPlan).
    - `routes/`: API endpoints.
    - `tests/`: Pytest suite.
- `mobile/`: React Native Expo app.
    - `app/`: Expo Router screens (index, onboarding, plan).
    - `constants/`: Design tokens (Colors).

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
