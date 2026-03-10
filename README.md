# Asset Management System

A simple web application for managing assets. The project features a FastAPI backend with SQLAlchemy for database management using SQLite, and a basic HTML/Bootstrap frontend to test backend actions.

## Features

- **FastAPI Backend**: Fast, modern, and asynchronous web framework for building APIs.
- **SQLAlchemy ORM (SQLite)**: Database models implemented for asset management (e.g., `AssetModel`). It leverages SQLite for a lightweight, file-based database.
- **Basic Frontend**: Includes a simple HTML and Bootstrap 5 frontend to test API actions.
- **API Endpoints**:
  - `/` - Root endpoint to check API status.
  - `/page` - Serves the frontend web page (`index.html`).
  - `/api/action` - A POST endpoint to test backend actions.
  - `/assets/` - Asset management endpoint.

## Project Structure

- `app/main.py`: The entry point for the FastAPI application.
- `app/api/`: Contains API routers (e.g., `assets.py`).
- `app/models/`: Contains SQLAlchemy database models (e.g., `asset.py`).
- `app/core/`: Core configurations like database engine and setup (`database.py`).
- `app/static/`: Contains static files like `index.html`.

## Getting Started

### Prerequisites

- Python 3.8+ (Make sure Python is added to your system PATH)
- Git (Optional)

### Complete Setup Instructions

Follow these exact steps to set up this workspace from scratch.

1. **Clone the repository (if applicable) and open the directory:**
   ```bash
   git clone <repository-url>
   cd Asset-Management
   ```

2. **Create a virtual environment:**
   Creating a virtual environment isolates your project dependencies from the global Python environment.
   
   *On Windows:*
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   *On macOS/Linux:*
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   Make sure you are in the virtual environment (you should see `(venv)` in your terminal prompt). Then, install the essential packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   You can start the Uvicorn server to serve the API and the web page:
   ```bash
   uvicorn app.main:app --reload
   ```

   *(The `--reload` flag ensures the server automatically restarts when you make code changes.)*

### Usage

- Open your browser and navigate to [http://localhost:8000/page](http://localhost:8000/page) to access the frontend application.
- Explore the interactive API documentation at [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI) or [http://localhost:8000/redoc](http://localhost:8000/redoc) (ReDoc).

### Database

The application is configured to use SQLite out of the box in `app/core/database.py` (`sqlite:///./asset_db.db`). 
When you run the application for the first time, a database file named `asset_db.db` will be automatically created in the root directory.
